

class WallController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_wall(self):
        entries = self.model.get_db_entries()
        self.view.refresh_img_wall(entries)
