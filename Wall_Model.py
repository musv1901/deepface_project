import requests


class WallModel:

    def __init__(self):
        self.db = {
            "url": "https://gc7da7be5da2e70-g833jueqvvi5nhsa.adb.eu-frankfurt-1.oraclecloudapps.com/ords/admin/persons",
            "headers": {
                "Content-type": "application/json",
                "Accept": "application/json"
            }
        }

    def get_db_entries(self):
        response = requests.get(self.db.get("url"), self.db.get("headers"))
        return response.json()["items"]
