import json
import time
from deepface import DeepFace
import cv2
from PIL import Image
from image2base64.converters import base64_to_rgb, rgb2base64
import multiprocessing as mp

def cameraFeed(cap):
    start_time = time.time()

    while True:

        ret, frame = cap.read()

        if time.time() - start_time >= 20:
            print("Start analyzing")
            p = mp.Pool(processes=1)
            p.apply_async(analyzeScreenshot, args=(frame, ))
            start_time = time.time()

        detectedFaces = DeepFace.extract_faces(img_path=frame, enforce_detection=False, detector_backend='opencv')

        for face in detectedFaces:
            x = face['facial_area']['x']
            y = face['facial_area']['y']
            w = face['facial_area']['w']
            h = face['facial_area']['h']

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def analyzeScreenshot(frame):
    result = DeepFace.analyze(img_path=frame, enforce_detection=False, detector_backend='mtcnn')

    p_list = {
        "persons": [

        ]
    }

    for face in result:
        cropped = getcroppedFace(face, frame)
        info = getpersonInfo(face, cropped)
        p_list["persons"].append(info)

        if not isPresent(cropped):
            storefaceHistory(info)

    with open("persons_present.json", "w") as file:
        json.dump(p_list, file)


def getpersonInfo(face_dict, cropped_face):
    return {
        "firstname": "",
        "lastname": "",
        "cropped_img_base": rgb2base64(cropped_face),
        "gender": face_dict.get('dominant_gender'),
        "age": str(face_dict.get('age')),
        "ethnicity": face_dict.get('dominant_race'),
        "emotion": face_dict.get('dominant_emotion')
    }


def storefaceHistory(face_info):
    with open("persons_history.json", "r") as file:
        data = json.load(file)

    data['persons'].append(face_info)

    with open("persons_history.json", "w") as file:
        json.dump(data, file)


def getcroppedFace(face_dict, frame):
    x = face_dict.get('region')['x']
    y = face_dict.get('region')['y']
    w = face_dict.get('region')['w']
    h = face_dict.get('region')['h']

    cropped_nd = frame[y:y + h, x:x + w]
    return Image.fromarray(cropped_nd)


def isPresent(cropped_face):
    with open("persons_history.json", "r") as file:
        data = json.load(file)

        for element in data['persons']:

            img = base64_to_rgb(element.get('cropped_img_base'), "PIL")

            img.save("temp1.jpeg", "JPEG")
            cropped_face.save("temp2.jpeg", "JPEG")
            dict = DeepFace.verify(img1_path="temp1.jpeg", img2_path="temp2.jpeg", detector_backend="mtcnn",
                                   enforce_detection=False)

            if dict['verified']:
                return True

        return False


if __name__ == "__main__":
    cap_feed = cv2.VideoCapture(0)

    cameraFeed(cap_feed)

