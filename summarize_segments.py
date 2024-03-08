import json
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def split_text(text, max_length=4000):
    """Splits the text into segments."""
    segments = []
    current_segment = ""
    for sentence in text.split('. '):
        if len(current_segment) + len(sentence) + 2 > max_length:
            segments.append(current_segment)
            current_segment = sentence
        else:
            if current_segment:
                current_segment += ". "
            current_segment += sentence
    if current_segment:
        segments.append(current_segment)
    return segments

def summarize_text(segment):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
                'role': "user",
                'content': f"Summarize this text:\n\n{segment}", }],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def find_highlights(segment, num_highlights=3):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
                'role': "user",
                'content': f"Extract {num_highlights} highlights from this text:\n\n{segment}",}],
        temperature=0.7,
        max_tokens=100
    )
    return response.choices[0].message.content.strip().split('\n')

def summarize_summaries(summaries):
    combined_summaries = " ".join(summaries)
    return summarize_text(combined_summaries)

# Load your transcript data
with open('transcriptions/Son estas lágrimas mi manjar-utterances.json', 'r') as file:
    transcript_data = json.load(file)

consolidated_text = " ".join([utterance['text_en'] for utterance in transcript_data])
segments = split_text(consolidated_text)

summaries = []
highlights_with_references = []
for i, segment in enumerate(segments):
    summary = summarize_text(segment)
    summary_highlights = find_highlights(segment)
    summaries.append(summary)
    for highlight in summary_highlights:
        # Append segment number for reference
        highlights_with_references.append((highlight, i+1))

# Summarize all summaries for a final overview
final_summary = summarize_summaries(summaries)

# Compile the final summary and highlight list into a dictionary
results = {
    "summary": final_summary,
    "highlights": [{"highlight": highlight, "segment_reference": reference} for highlight, reference in highlights_with_references]
}

# Define the filename for the output JSON file
output_filename = 'podcast_summary_and_highlights.json'

# Write the results to a JSON file
with open(output_filename, 'w') as outfile:
    json.dump(results, outfile, indent=4)

print(f"Results saved to {output_filename}")
