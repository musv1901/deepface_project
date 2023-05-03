import json
import time
from deepface import DeepFace
import cv2
from PIL import Image, ImageTk
from image2base64.converters import base64_to_rgb, rgb2base64
import multiprocessing as mp
from confluent_kafka import Producer, Consumer
import csv
from datetime import datetime


def camera_feed(feed):

    ret, frame = feed.read()

    detectedFaces = DeepFace.extract_faces(img_path=frame, enforce_detection=False, detector_backend='opencv')

    for face in detectedFaces:
        if face['confidence'] > 5:

            x = face['facial_area']['x']
            y = face['facial_area']['y']
            w = face['facial_area']['w']
            h = face['facial_area']['h']

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    return ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

    # cv2.imshow("frame", frame)


def analyze_screenshot(frame):
    result = DeepFace.analyze(img_path=frame, enforce_detection=False, detector_backend='mtcnn')

    p_list = {
        "persons": [

        ]
    }

    for face in result:
        cropped = get_cropped_face(face, frame)
        info = get_person_info(face, cropped)
        p_list["persons"].append(info)

        if not is_present(cropped):
            store_face_history(info)

    with open("persons_present.json", "w") as file:
        json.dump(p_list, file)


def get_person_info(face_dict, cropped_face):
    return {
        "firstname": "",
        "lastname": "",
        "cropped_img_base": rgb2base64(cropped_face),
        "gender": face_dict.get('dominant_gender'),
        "age": str(face_dict.get('age')),
        "ethnicity": face_dict.get('dominant_race'),
        "emotion": face_dict.get('dominant_emotion')
    }


def store_face_history(face_info):
    with open("persons_history.json", "r") as file:
        data = json.load(file)

    data['persons'].append(face_info)

    with open("persons_history.json", "w") as file:
        json.dump(data, file)


def get_cropped_face(face_dict, frame):
    x = face_dict.get('region')['x']
    y = face_dict.get('region')['y']
    w = face_dict.get('region')['w']
    h = face_dict.get('region')['h']

    cropped_nd = frame[y:y + h, x:x + w]
    return Image.fromarray(cropped_nd)


def is_present(cropped_face):
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


def get_persons_statistics():
    sum_age = 0
    male_count = 0

    with open("persons_present.json", "r") as file:
        data = json.load(file)

    for element in data['persons']:
        sum_age = sum_age + float(element.get("age"))

        if element.get("gender") == "Man":
            male_count = male_count + 1

    avg_age = sum_age / len(data['persons'])
    male_percentage = float(male_count / len(data['persons'])) * 100
    woman_percentage = 100 - male_percentage

    timestamp = time.time()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%d-%m-%Y %H:%M:%S")

    pers_stats = {
        "timestamp": str_date_time,
        "avg_age": avg_age,
        "male_percentage": male_percentage,
        "woman_percentage": woman_percentage
    }

    create_timestamp(pers_stats)

    return pers_stats


def create_timestamp(pers_stats):
    field_names = ['timestamp', 'avg_age', 'male_percentage', 'woman_percentage']

    with open('stats_history.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writerow(pers_stats)


def read_ccloud_config():
    conf = {}
    with open("kafka_config.txt", "r") as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != '#':
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    print(conf)
    return conf


def get_producer(conf):
    return Producer(conf)


def get_consumer(conf):
    conf["group.id"] = "python-group-1"
    conf["auto.offset.reset"] = "earliest"

    return Consumer(conf)


def produce_to_analyze(msg):
    producer.produce("toAnalyze", key="1", value=msg)
    producer.flush()


if __name__ == "__main__":
    get_persons_statistics()

    kafka_conf = read_ccloud_config()
    producer = get_producer(kafka_conf)
    # consumer = get_consumer(kafka_conf)

    # produce_to_analyze("Test_MSG")

    # cap_feed = cv2.VideoCapture(0)

    # camera_feed(cap_feed)
