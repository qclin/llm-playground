import spacy
import os
from typing import List
import json 

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

def load_transcripts(directory: str) -> List[str]:
    transcripts = []
    for filename in os.listdir(directory):
        if filename.endswith("fitness_utterances.json"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                transcripts.append(data)
    return transcripts

def process_transcripts(transcripts: List[str]):
    """Process transcripts and print named entities."""
    for transcript in transcripts:
        text_en_list = [utterance["text_en"] for utterance in transcript["utterances"]]
        # Join the extracted text_en fields into a single string
        combined_text = " ".join(text_en_list)
        doc = nlp(combined_text)
        for ent in doc.ents:
            print(f"Entity: {ent.text}, Label: {ent.label_}")

def main(): 
    # Directory containing transcript files
    transcript_directory = "transcriptions/season_1/"
    transcripts = load_transcripts(transcript_directory)
    process_transcripts(transcripts)
    
# Load transcripts
if __name__ == '__main__':
    main()