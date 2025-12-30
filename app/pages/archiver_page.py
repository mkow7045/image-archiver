from common import *
from app.widgets import Gallery
import os

class Archiver(QWidget):
    def __init__(self, state_manager, database_manager):
        super().__init__()
        self.database_manager = database_manager
        self.state_manager = state_manager
        self.layout = QVBoxLayout()
        self.tag_chooser = QLineEdit()
        self.tag_chooser.setPlaceholderText("Filter")
        self.gallery = Gallery()
        self.layout.addWidget(self.tag_chooser)
        self.layout.addWidget(self.gallery)
        self.setLayout(self.layout)

        self.tag_chooser.returnPressed.connect(self.get_images_from_db)
        self.get_images_from_db()
        
    def get_images_from_db(self):
        filter_yes = []
        filter_no = []
        conf = ""
        conf_supplied = False
        filters = self.tag_chooser.text().split()
        if filters:
            conf = filters[0]
            if "conf=" in conf:
                conf = conf[5:]
                filters = filters[:0] + filters[1:]
            try:
                conf = float(conf)
                if conf < 0.0 or conf > 1.0:
                    raise ValueError()
                conf_supplied = True
            except ValueError:
                conf_supplied = False

        if conf_supplied:
            self.state_manager.conf_filter = conf
        else:
            self.state_manager.conf_filter = 0.0

        for filter in filters:
            if filter[0] == "-":
                filter_no.append(filter[1:])
            else:
                filter_yes.append(filter)

        self.state_manager.filter_yes = filter_yes
        self.state_manager.filter_no = filter_no
        
        rows = self.database_manager.choose_from_db(filter_yes,filter_no)


        image_list = [os.path.join("images",row[0]) for row in rows]
        image_list = list(dict.fromkeys(image_list))
        self.gallery.update_images(image_list)



        
