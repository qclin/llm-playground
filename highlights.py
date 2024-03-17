from openai import OpenAI
import os
from scripts.process_json import load_json, write_json, check_json_file
import json

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


def find_highlights_and_entities(chunk):
    prompt_for_analysis = (
        "Analyze a list of transcriptions and their sequence numbers to identify key topics with corresponding sequences, "
        "mention all entities (people, places, organizations, events, etc.) including the type of entity and all sequence numbers where each entity is mentioned, "
        "and specifically identify any citations of literature (books, articles, authors, publication details) along with the sequence number each citation is mentioned in. "
        "For entities, organize them into objects with 'entity', 'type', and 'sequences', where 'sequences' is a list of all unique sequence numbers the entity appears in. "
        "Return a JSON object with 'topics', each containing 'topic' and a range of 'sequences' associated with it; 'entities', a list of such objects; "
        "and 'citations', a list of objects with 'citation' details and 'sequence'. Ensure 'sequences' for topics are ranges (e.g., '1-5'), while for entities, 'sequences' should list all appearances, and for citations, include specific sequence numbers."
    )

    response = client.chat.completions.create(
        response_format={ "type": "json_object" }, 
        model="gpt-4-0125-preview",
        messages=[{
            "role": "system",
            "content": prompt_for_analysis
        },
        {
            "role": "user",
            "content": f"Here's a list of transcripts: {chunk}. Based on the instruction, identify and organize the topics and entities."

        }],
        max_tokens=2056,
        temperature=0,
        frequency_penalty=0,
        presence_penalty=0,

    )
    
   

    try:
        content = response.choices[0].message.content
        parsed_content = json.loads(content)
        return parsed_content
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    

def deduplicate_citations(citations):
    unique_citations = []
    seen = set()
    for citation in citations:
        # Assuming each citation dict has a 'title' and 'author' keys
        # Adjust the identifier as needed based on your citation structure
        identifier = (citation.get('title'), citation.get('author'))
        if identifier not in seen:
            seen.add(identifier)
            unique_citations.append(citation)
    return unique_citations


def main(input_file, output_file): 
    # Load the transcript data from the uploaded JSON file
    transcript_data = load_json(input_file)

    input_data = [{"text": subtitle['text_en'], "sequence": subtitle['sequence']} for subtitle in transcript_data]
    # Split the transcript data into chunks
    chunks = split_into_chunks(input_data)

    all_highlights_with_sequences = []
    all_entities = []
    all_citations = []
    for chunk in chunks:
        analysis_results = find_highlights_and_entities(chunk)
        # Separate the processing of highlights and entities based on the new function output
        all_highlights_with_sequences.extend(analysis_results['topics'])
        all_entities.extend(analysis_results['entities'])
        all_citations.extend(analysis_results['citations'])

    # Deduplicate citations 
    unique_citations = deduplicate_citations(all_citations)  # Assuming direct deduplication is applicable

    results = {
        'topics': all_highlights_with_sequences,
        'entities': all_entities, 
        'citations': unique_citations
    }
    # Continue with writing results to file as previously shown
    write_json(results, output_file)