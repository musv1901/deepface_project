from Wall_Controller import WallController
from Wall_Model import WallModel
from Wall_View import WallView

if __name__ == "__main__":
    model = WallModel()
    view = WallView()
    controller = WallController(model=model, view=view)

    while True:
        controller.update_wall()
        view.window.update()