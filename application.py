import os
from flask import Flask, jsonify, request, abort
from scripts.process_json import load_json

app = Flask(__name__)

@app.route('/season', methods=['GET'])
def get_all_season():
    combined_data = {}

    for i in range(1, 5):
        file_path = f'./transcriptions/las_hijas_overview_season_{i}.json'
        data = load_json(file_path)
        combined_data[f'season_{str(i)}'] = data

    return jsonify(combined_data)

@app.route('/season/<path:id>', methods=['GET'])
def get_season_list(id):

    if id is None or type(int(id)) is not int:
        abort(400, description="Missing required parameters")
    
    # Check if file exists
    file_path = f'./transcriptions/las_hijas_overview_season_{int(id)}.json'
    if not os.path.exists(file_path):
        abort(404, description="JSON file not found")

    season_summary = load_json(file_path)
    processed_data = season_summary
    
    return jsonify(processed_data)


@app.route('/episode', methods=['GET'])
def get_episode_transcript():
    # Get query parameters from the request
    title = request.args.get('title')
    season = request.args.get('season')
    
    if title is None or season is None:
        abort(400, description="Missing required parameters")

    # Check if JSON file exists
    transcript_file_path = f'./transcriptions/season_{season}/{title}_utterances.json'
    highlight_file_path = f'./transcriptions/season_{season}/{title}_topics.json'

    if not os.path.exists(transcript_file_path) or not os.path.exists(highlight_file_path):
        abort(404, description="JSON file not found")

    transcript_data = load_json(transcript_file_path)
    highlight_data = load_json(highlight_file_path)
    processed_data = {"transcription": transcript_data, "highlights": highlight_data}
    
    return jsonify(processed_data)

if __name__ == '__main__':
    app.run(debug=True)


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": error.description}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": error.description}), 404

@app.errorhandler(Exception)
def server_error(error):
    return jsonify({"error": "Server Error", "message": "An internal server error occurred"}), 500
