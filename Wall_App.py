import time
from Wall_Controller import WallController
from Wall_Model import WallModel
from Wall_View import WallView

if __name__ == "__main__":
    model = WallModel()
    view = WallView()
    controller = WallController(model=model, view=view)
    controller.update_wall()

    start = time.time()
    while True:
        if int(time.time() - start) > 10:
            controller.update_wall()
            start = time.time()
        view.window.update()

