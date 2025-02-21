from flask import Flask, render_template, jsonify
import json
import app.function as function
from flask import Flask
import time
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

USERNAME="2n3vohg923lg7ustb6fang577"

@app.route('/')
def home():
    try:
        with open('token.json','r') as file:
            data=json.load(file)
        current_time=time.time()
        if current_time>data['token_expire_time']:
            function.getAccessToken()
        
    except:
        function.getAccessToken()
        with open('token.json','r') as file:
            data=json.load(file)
    return render_template('index.html')

@app.route('/detect-mood')
def detecMood():
    response=function.addToSpotify(USERNAME)
    return f"""
        <a href="{response}" target="_blank">Click This Link To get Your Playlist</a>
    """

if __name__ == '__main__':
    app.run(debug=True)