from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Run the script
        subprocess.run(['python', 'sixthlane.py'], check=True)
        message = 'Engine is ready and set.'
    except subprocess.CalledProcessError:
        message = 'Engine failed, check with the mechanic.'
    return render_template('index.html', message=message)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)