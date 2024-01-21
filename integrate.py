# app.py
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import subprocess
import json


app = Flask(__name__)
CORS(app)

def getJsonData():
    with open('currentEmotionSongs.json','r') as json_file:
        data=json.load(json_file)
    return data

@app.route('/')
def index():
    return "Test SucessFull"

@app.route('/run_process')
def run_process():
    subprocess.run(['python', 'emotion.py'])
    data=getJsonData()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
