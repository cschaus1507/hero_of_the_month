from flask import Flask, request, jsonify
import json, os
from collections import Counter

app = Flask(__name__)
VOTE_FILE = 'votes.json'

# Create votes.json if it doesn't exist
if not os.path.exists(VOTE_FILE):
    with open(VOTE_FILE, 'w') as f:
        json.dump([], f)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    hero = data.get('hero')
    if not hero:
        return jsonify({'error': 'No hero provided'}), 400

    with open(VOTE_FILE, 'r+') as f:
        votes = json.load(f)
        votes.append(hero)
        f.seek(0)
        json.dump(votes, f)
        f.truncate()

    return jsonify({'message': 'Vote received'}), 200

@app.route('/results', methods=['GET'])
def results():
    with open(VOTE_FILE, 'r') as f:
        votes = json.load(f)
    tally = Counter(votes)
    return jsonify(tally.most_common())

@app.route('/reset', methods=['POST'])
def reset():
    with open(VOTE_FILE, 'w') as f:
        json.dump([], f)
    return jsonify({'message': 'Votes reset'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
