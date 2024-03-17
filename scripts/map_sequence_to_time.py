from .process_json import load_json, write_json

# Function to parse sequence ranges into start and end integers
def parse_sequences(sequence_str):
    parts = sequence_str.split('-')
    start_seq = int(parts[0])
    end_seq = int(parts[-1]) if len(parts) > 1 else start_seq
    return start_seq, end_seq


def map_sequence_to_time(utterances_path, topics_path): 
    # Initialize a list to hold the mapping of topics to their start and end times
    topics_with_times = []
    utterances_data = load_json(utterances_path)
    file_data = load_json(topics_path)


    # Iterate through each topic and map it to its start and end times based on the sequence numbers
    for topic in file_data["topics"]:
        topic_name = topic["topic"]
        if 'sequences' not in topic: return
        sequence_range = topic["sequences"]
        start_seq, end_seq = parse_sequences(sequence_range)
        
        # Find utterances that fall within this sequence range and determine their start and end times
        start_times = []
        end_times = []
        for utterance in utterances_data:
            if start_seq <= utterance["sequence"] <= end_seq:
                start_times.append(utterance["start"])
                end_times.append(utterance["end"])
        
        # Determine the overall start and end time for the topic
        if start_times and end_times:  # Ensure there are times to calculate min/max from
            overall_start_time = min(start_times)
            overall_end_time = max(end_times)
            topics_with_times.append({
                "topic": topic_name,
                "sequence_range": sequence_range,
                "start_time": overall_start_time,
                "end_time": overall_end_time
            })

    file_data["topics"] = topics_with_times
    write_json(file_data, topics_path)