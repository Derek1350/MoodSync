import test
import json
import random
import cv2
import numpy as np
from keras.models import load_model
import time
import os


emotion=test.emotionDetection().lower()
script_path = os.path.abspath(__file__)
json_file_path = os.path.join(os.path.dirname(script_path), 'songs_data', f'{emotion}Songs.json')


with open(json_file_path,'r',encoding='utf-8') as json_file:
    data=json.load(json_file)

songsDetailsList=list(data.items())
songsDetails=random.sample(songsDetailsList,11)
song_names = [item[1] for item in songsDetails if item[0].startswith('name')]
while len(song_names) < 11:
    additional_samples = random.sample(songsDetailsList, 11 - len(song_names))
    additional_names = [item[1] for item in additional_samples if item[0].startswith('name')]
    song_names.extend(additional_names)
print(song_names)
songsName={}
for i in range(0,10):
    songsName[f'song {i}']=song_names[i]
with open('currentEmotionSongs.json','w') as file:
    json.dump(songsName,file)