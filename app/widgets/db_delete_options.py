from common import *

class DatabaseDelete(QDialog):

    def __init__(self, database_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Database Options")
        self.setModal(True)

        layout = QVBoxLayout()

        self.database_manager = database_manager

        self.current_selection = QRadioButton("Delete current selection from database")
        self.all_images = QRadioButton("Delete all entires from database")
        self.accept_choice = QPushButton("DELETE(THIS ACTION IS PERMANENT!)")
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.current_selection,1)
        self.button_group.addButton(self.all_images,2)

        layout.addWidget(self.current_selection)
        layout.addWidget(self.all_images)
        layout.addWidget(self.accept_choice)

        self.accept_choice.clicked.connect(self.handle_delete)

        self.setLayout(layout)

    def handle_delete(self):
        delete_all = False
        selected = self.button_group.checkedId()
        if selected == 1:
            self.database_manager.delete_from_db(delete_all)
        if selected == 2:
            delete_all = True
            self.database_manager.delete_from_db(delete_all)

        self.close()

        
