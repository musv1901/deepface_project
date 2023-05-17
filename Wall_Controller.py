import requests

class WallController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.db = {
            "url": "https://gc7da7be5da2e70-g833jueqvvi5nhsa.adb.eu-frankfurt-1.oraclecloudapps.com/ords/admin/persons",
            "headers": {
                "Content-type": "application/json",
                "Accept": "application/json"
            }
        }

    def update_wall(self):
        response = requests.get(self.db.get("url"), self.db.get("headers"))
        #self.view.refresh_img_wall(response.json()["items"])
