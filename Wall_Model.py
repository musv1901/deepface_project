import json

import requests


class WallModel:

    def __init__(self):
        self.db = {
            "get_rows_sorted": "https://gc7da7be5da2e70-g833jueqvvi5nhsa.adb.eu-frankfurt-1.oraclecloudapps.com/ords/admin/operations/return_rows_sorted",
            "insert_name": "https://gc7da7be5da2e70-g833jueqvvi5nhsa.adb.eu-frankfurt-1.oraclecloudapps.com/ords/admin/operations/insert_name",
            "headers": {
                "Content-type": "application/json",
                "Accept": "application/json"
            }
        }

    def get_db_entries(self):
        response = requests.get(self.db.get("get_rows_sorted"), self.db.get("headers"))
        return response.json()["items"]

    def insert_name_db(self, p_id, p_name):
        payload = {
            "in_id": p_id,
            "in_name": p_name
        }

        r = requests.post(self.db.get("insert_name"), json.dumps(payload), headers=self.db.get("headers"))
        print(payload)
        print(r.status_code)


