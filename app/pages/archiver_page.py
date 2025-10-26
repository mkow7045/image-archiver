from common import *
from app.widgets import Gallery
import os

class Archiver(QWidget):
    def __init__(self, state_manager, database_manager):
        super().__init__()
        self.database_manager = database_manager
        self.layout = QVBoxLayout()
        self.tag_chooser = QLineEdit()
        self.tag_chooser.setPlaceholderText("Filter")
        self.gallery = Gallery()
        self.layout.addWidget(self.tag_chooser)
        self.layout.addWidget(self.gallery)
        self.setLayout(self.layout)

        self.tag_chooser.returnPressed.connect(self.get_images_from_db)
        
    def get_images_from_db(self):
        filter_yes = []
        filter_no = []
        filters = self.tag_chooser.text().split()
        for filter in filters:
            if filter[0] == "-":
                filter_no.append(filter[1:])
            else:
                filter_yes.append(filter)

        rows = self.database_manager.choose_from_db(filter_yes,filter_no)
        image_list = [os.path.join("images",row[1]) for row in rows]
        image_list = list(dict.fromkeys(image_list))
        self.gallery.update_images(image_list)



        
