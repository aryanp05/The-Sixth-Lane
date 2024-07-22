from flask import Flask, render_template, redirect, url_for
import os
from spotify_script import update_playlist
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-script', methods=["POST"])
def run_script():
    try:
        update_playlist()
        return "Playlist updated successfully!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
