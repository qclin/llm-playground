from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/items', methods=['GET'])
def get_items():
    items = ["apple", "banana", "cherry"]
    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True)
