import openai
import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def summarize_podcast(translated_subtitles):
    """
    Summarize the podcast using ChatGPT-4.
    """
    # Concatenate all translated subtitles into one string
    # all_translated_text = " ".join(subtitle['text_en'] for subtitle in translated_subtitles)
    input_data = [{"text": subtitle['text_en'], "sequence": subtitle['sequence']} for subtitle in translated_subtitles]

    # Use ChatGPT-4 to summarize the podcast
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
          messages=[
              {
                'role': "user",
                'content': f"Summarize the following podcast transcription {input_data} and find highlights and fun facts they discussed, output the results as json"
                }
        ],
        max_tokens=2048,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    
    summary = response.choices[0].message.content.strip()
    
    print(f'summary: {summary}'); 
    return summary

# Example usage
if __name__ == "__main__":
    # Load translated subtitles from a JSON file
    with open("transcriptions/Son estas lágrimas mi manjar-utterances.json", "r") as file:
        translated_subtitles = json.load(file)

    # Summarize the podcast
    podcast_summary = summarize_podcast(translated_subtitles)
    # Save the response in JSON format
    response = {
        "summary": podcast_summary,
    }

    with open("transcriptions/podcast_summary.json", "w") as output_file:
        json.dump(response, output_file, indent=4)

    print("Podcast summary and themes saved in podcast_summary.json")
