from flask import Flask, jsonify
import json
import random

app = Flask(__name__)

with open("highlights.json", encoding="utf-8") as f:
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