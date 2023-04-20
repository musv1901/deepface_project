import json
import time
from deepface import DeepFace
import cv2
import uuid
import base64
import io
from io import BytesIO
import tkinter as tk
import customtkinter
from PIL import Image


def getImage(frame):
    result = DeepFace.analyze(img_path=frame, enforce_detection=False, detector_backend='mtcnn')
    print(result)

    for face in result:
        print(face)
        txt = 'Gender: ' + face.get('dominant_gender') + '\n' \
              + 'Age: ' + str(face.get('age')) + '\n' \
              + 'ethnicity: ' + face.get('dominant_race') + '\n' \
              + 'Emotion: ' + face.get('dominant_emotion')

        print(txt)

        x = face.get('region')['x']
        y = face.get('region')['y']
        w = face.get('region')['w']
        h = face.get('region')['h']

        cropped_img = frame[y:y + h, x:x + w]
        #isPresent(cropped_img)

        _, im_arr = cv2.imencode('.jpeg', cropped_img)
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)

        person = {
            "firstname": "",
            "lastname": "",
            "cropped_img_base": str(im_b64),
            "gender": face.get('dominant_gender'),
            "age": str(face.get('age')),
            "ethnicity": face.get('dominant_race'),
            "emotion": face.get('dominant_emotion')
        }

        with open("persons.json", "r") as file:
            data = json.load(file)

        data['persons'].append(person)

        with open("persons.json", "w") as file:
            json.dump(data, file)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

        cv2.imshow('Cropped', cropped_img)
        cv2.putText(frame, txt, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        # saveImage(frame)
    # cv2.imshow('Picture', frame)

    time.sleep(30)


def saveImage(frame):
    cv2.imwrite('Pictures\img' + str(uuid.uuid4()) + '.jpg', frame)


def isPresent(face):
    with open("persons.json", "r") as file:
        data = json.load(file)

    for element in data['persons']:
        decode = base64.b64decode(element.get('cropped_img_base'))

        #img = Image.open(io.BytesIO(decode))
        #img = Image.frombytes(decode)
        #img.save("temp1.jpeg", "JPEG")
        #cv2.imwrite("temp2.jpeg", face)
        #print(DeepFace.verify(img1_path="temp1.jpeg", img2_path="temp2.jpeg", detector_backend="mtcnn"))


if __name__ == "__main__":

    # root = tk.Tk()

    # root.geometry('1000x500')
    # root.title('Visitor Dashboard')

    # label = tk.Label(root, text='Hello Visitor!', font=('Arial', 18))
    # label.pack(padx=20, pady=20)

    # root.mainloop()
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        getImage(frame)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
