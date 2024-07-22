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
        message = 'Script executed successfully!'
    except subprocess.CalledProcessError:
        message = 'An error occurred while running the script.'
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
