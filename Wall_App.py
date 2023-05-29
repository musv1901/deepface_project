import time
from Wall_Model import WallModel
from Wall_View import WallView
from confluent_kafka import Consumer

if __name__ == "__main__":
    model = WallModel()
    view = WallView(model)
    p_list = model.get_db_entries()
    view.refresh_img_wall(p_list)

    consumer = Consumer({
        'bootstrap.servers': '192.168.70.40:9092',
        'group.id': 'py',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['toUI'])

    start = time.time()
    while True:
        if len(consumer.assignment()) != 0 and not view.refresh_stop:
            print("Info message")
            p_list = model.get_db_entries()
            view.refresh_img_wall(p_list)
            consumer.consume(1)
            #view.start_time = time.time()
        view.window.update()
