import json

utterances_path = 'transcriptions/Disecciones conventuales, anatomía barroca-utterances.json'
topics_path = 'transcriptions/anatomy_topics.json'

with open(utterances_path, 'r', encoding='utf-8') as file:
    utterances_data = json.load(file)

with open(topics_path, 'r', encoding='utf-8') as file:
    topics_data = json.load(file)


# Initialize a list to hold the mapping of topics to their start and end times
topics_with_times = []

# Function to parse sequence ranges into start and end integers
def parse_sequences(sequence_str):
    parts = sequence_str.split('-')
    start_seq = int(parts[0])
    end_seq = int(parts[-1]) if len(parts) > 1 else start_seq
    return start_seq, end_seq

# Iterate through each topic and map it to its start and end times based on the sequence numbers
for topic in topics_data["topics"]:
    topic_name = topic["topic"]
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


# Define the filename for the output JSON file
output_filename = 'transcriptions/anatomy_topics.json'

results = {'topics': topics_with_times}
# Write the results to a JSON file
with open(output_filename, 'w') as outfile:
    json.dump(results, outfile, indent=4)