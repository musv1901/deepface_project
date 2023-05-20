import time
from Wall_Model import WallModel
from Wall_View import WallView

if __name__ == "__main__":
    model = WallModel()
    view = WallView()
    p_list = model.get_db_entries()
    view.refresh_img_wall(p_list)

    while True:
        if int(time.time() - view.start_time) > 10 and not view.refresh_stop:
            p_list = model.get_db_entries()
            view.refresh_img_wall(p_list)
            view.start_time = time.time()
        view.window.update()
