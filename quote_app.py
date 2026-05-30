from flask import Flask, jsonify
import json
import random
import os

app = Flask(__name__)

# Load highlights using the directory of this file
base_dir = os.path.dirname(os.path.abspath(__file__))
highlights_path = os.path.join(base_dir, "highlights.json")

with open(highlights_path, encoding="utf-8") as f:
    highlights = json.load(f)

@app.route("/quote")
def quote():
    pick = random.choice(highlights)
    return jsonify({
        "book": pick["book"],
        "quote": pick["quote"]
    })

if __name__ == "__main__":
    app.run()