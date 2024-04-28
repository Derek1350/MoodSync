import cv2
import numpy as np
from keras.models import load_model
import time
from collections import Counter
import json
import random
import os
import requests
from dotenv import load_dotenv
load_dotenv()

refresh_token=os.getenv("refresh_token")

def getAccessToken():
    refresh_token_url=f"https://spotify-api-authorize.onrender.com/refresh-token?refresh_token={refresh_token}"
    response=requests.get(url=refresh_token_url)
    with open('token.json','w') as file:
        json.dump(response.json(),file)

def emotionDetection(duration):
    model = load_model('model_file_30epochs.h5')

    video = cv2.VideoCapture(0)
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Sad', 6: 'Surprise'}

    emotions_list = []

    start_time = time.time()

    while (time.time() - start_time) < duration:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 3)

        for x, y, w, h in faces:
            sub_face_img = gray[y:y + h, x:x + w]
            resized = cv2.resize(sub_face_img, (48, 48))
            normalize = resized / 255.0
            reshaped = np.reshape(normalize, (1, 48, 48, 1))
            result = model.predict(reshaped)
            label = np.argmax(result, axis=1)[0]
            emotion = labels_dict[label]
            emotions_list.append(emotion)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Emotion Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    emotion_counts = Counter(emotions_list)

    most_common_emotion = emotion_counts.most_common(1)[0][0]

    print(f"Emotions collected: {emotions_list}")
    print(f"Most occurred emotion: {most_common_emotion}")
    
    return most_common_emotion

def currentEmotionSongs():
    emotion=emotionDetection(5).lower()

    with open(f'./songs_data/{emotion}Songs.json','r',encoding='utf-8') as json_file:
        data=json.load(json_file)['items']

    random_selected_songs=random.sample(data,10)

    final_selected_songs={}
    selected_songs_uri=[]

    
    for i in random_selected_songs:
        final_selected_songs[i['track']['name']]=i['track']['uri']
        selected_songs_uri.append(str(i['track']['uri']))

    with open('currentEmotionSongs.json','w') as file:
        json.dump(final_selected_songs,file)
    return [emotion,selected_songs_uri]

def addToSpotify(USERNAME):
    with open('token.json','r') as file:
        data=json.load(file)
    data_currentEmotionSongs=currentEmotionSongs()
    emotion=data_currentEmotionSongs[0]
    selected_songs_uri=data_currentEmotionSongs[1]
    print(emotion,selected_songs_uri)
    print(data['access_token'])
    create_playlist_url=f'https://api.spotify.com/v1/users/{USERNAME}/playlists'
    create_playlist_body={
        "name": f'Suggested {emotion} Songs',
        "description": "Generated Songs According To The Current Mood",
        "public": False
    }
    create_playlist_headers={
        "Authorization":f'Bearer {data["access_token"]}',
        "Content-Type":"application/json"
    }
    response=requests.post(create_playlist_url,headers=create_playlist_headers,json=create_playlist_body)
    created_playlist_url=response.json()["external_urls"]["spotify"]
    if response.status_code == 201:
        created_playlist_id=response.json()['id']
        add_songs_url=f'https://api.spotify.com/v1/playlists/{created_playlist_id}/tracks'
        add_songs_body={
            "uris":selected_songs_uri,
            "position":0
        }
        response=requests.post(url=add_songs_url,headers=create_playlist_headers,json=add_songs_body)
        return created_playlist_url
    else:
       return response.json()
