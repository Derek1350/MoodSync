import cv2
import numpy as np
from keras.models import load_model
import time
from collections import Counter

def emotionDetection(duration=5):
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

    # Count occurrences of each emotion
    emotion_counts = Counter(emotions_list)

    # Get the most occurred emotion
    most_common_emotion = emotion_counts.most_common(1)[0][0]

    print(f"Emotions collected: {emotions_list}")
    print(f"Most occurred emotion: {most_common_emotion}")

    return most_common_emotion

# if __name__ == "__main__":
#     emotionDetection(duration=5)




# import cv2
# import numpy as np
# from keras.models import load_model
# import time

# def emotionDetection():

#     model = load_model('model_file_30epochs.h5')

#     video = cv2.VideoCapture(0)
#     faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#     labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Sad', 6: 'Surprise'}

#     while True:
#         ret, frame = video.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = faceDetect.detectMultiScale(gray, 1.3, 3)

#         for x, y, w, h in faces:
#             sub_face_img = gray[y:y + h, x:x + w]
#             resized = cv2.resize(sub_face_img, (48, 48))
#             normalize = resized / 255.0
#             reshaped = np.reshape(normalize, (1, 48, 48, 1))
#             result = model.predict(reshaped)
#             label = np.argmax(result, axis=1)[0]
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
#             cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
#             cv2.putText(frame, labels_dict[label], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

#             emotion = labels_dict[label]
#             print(f"Emotion: {emotion}")

#         cv2.imshow("Emotion Detection", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break



#     video.release()
#     cv2.destroyAllWindows()
#     return emotion
# if __name__ == "__main__":
#     emotionDetection()