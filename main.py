import json
import time
from deepface import DeepFace
import cv2
import uuid
import base64


def getImage():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

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
            _, im_arr = cv2.imencode('.jpg', cropped_img)
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


            # Writing to sample.json
            with open("persons.json", "r") as file:
                data = json.load(file)

            data['persons'].append(person)

            with open("persons.json", "w") as file:
                json.dump(data, file)
                #print(data['persons'])
                #outfile.write(json_object)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

            cv2.imshow('Cropped', cropped_img)
            cv2.putText(frame, txt, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            # saveImage(frame)
        # cv2.imshow('Picture', frame)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break
        time.sleep(10)

    cap.release()
    cv2.destroyAllWindows()


def saveImage(frame):
    cv2.imwrite('Pictures\img' + str(uuid.uuid4()) + '.jpg', frame)


getImage()
