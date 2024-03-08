from openai import OpenAI
import os
from scripts.process_json import load_json, write_json

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Assuming each object in the list has a 'text' field that we want to consider for the token count
# and that we have already loaded a JSON object into `transcript_data`

def split_into_chunks(data, max_tokens=4096):
    """
    Splits a list of objects into chunks where the total token count of the 'text_en' field in each chunk does not exceed max_tokens.
    Each object's 'text' field is assumed to be the source of tokens.
    """
    chunks = []
    current_chunk = []
    current_token_count = 0
    
    for item in data:
        item_text = item['text']
        item_tokens = len(item_text.split())  # Naive token count based on spaces
        
        if current_token_count + item_tokens > max_tokens:
            # Current item would exceed the max token limit; start a new chunk
            chunks.append(current_chunk)
            current_chunk = [item]
            current_token_count = item_tokens
        else:
            # Add the current item to the existing chunk
            current_chunk.append(item)
            current_token_count += item_tokens
    
    # Don't forget to add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def find_highlights(chunk):
    response = client.chat.completions.create(
        response_format={ "type": "json_object" }, 
        model="gpt-4-0125-preview",
        messages=[{
            "role": "system",
            "content": "Analyze a list of transcriptions and their sequence numbers to identify key topics and corresponding sequences."
        },
        {
            "role": "user",
            "content": f"Here's a list of transcripts: {chunk}. Find topics of interest and points of references and group sequences by theme. Return a JSON list with each object containing 'topics' and a range of 'sequences' associated with it, where sequences is not a list but a range."
        }],
        max_tokens=1028,
        temperature=0,
        frequency_penalty=0,
        presence_penalty=0,

    )
    
    return response.choices[0].message.content.strip().split('\n')


def main(file_name): 
    # Load the transcript data from the uploaded JSON file
    file_path = f'transcriptions/{file_name}_utterances.json'
    transcript_data = load_json(file_path)

    input_data = [{"text": subtitle['text_en'], "sequence": subtitle['sequence']} for subtitle in transcript_data]
    # Split the transcript data into chunks
    chunks = split_into_chunks(input_data)

    highlights_with_sequences = []
    for chunk in chunks:
        summary_highlights = find_highlights(chunk)
        highlights_with_sequences.append(summary_highlights)

    results = {'topics': highlights_with_sequences}
    output_filename = f'transcriptions/{file_name}_topics.json'
    write_json(results, output_filename)