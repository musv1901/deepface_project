import time
from Wall_Model import WallModel
from Wall_View import WallView

if __name__ == "__main__":
    model = WallModel()
    view = WallView()
    p_list = model.get_db_entries()
    view.refresh_img_wall(p_list)

    start = time.time()
    while True:
        if int(time.time() - start) > 10:
            p_list = model.get_db_entries()
            view.refresh_img_wall(p_list)
            start = time.time()
        view.window.update()

