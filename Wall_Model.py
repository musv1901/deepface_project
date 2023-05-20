import requests


class WallModel:

    def __init__(self):
        self.db = {
            "get_rows_sorted": "https://gc7da7be5da2e70-g833jueqvvi5nhsa.adb.eu-frankfurt-1.oraclecloudapps.com/ords/admin/operations/return_rows_sorted",
            "headers": {
                "Content-type": "application/json",
                "Accept": "application/json"
            }
        }

    def get_db_entries(self):
        response = requests.get(self.db.get("get_rows_sorted"), self.db.get("headers"))
        return response.json()["items"]

    def insert_name(self, p_id, name):
        print(name + "for ID: " + p_id)
