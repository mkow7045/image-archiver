from common import *
from datetime import datetime

class ExportOptions(QDialog):

    def __init__(self, database_manager, state_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export options")
        self.setModal(True)

        self.setMinimumSize(650,300)

        self.state_manager = state_manager

        self.class_names = self.state_manager.class_names

        self.choosen_folder = ""

        layout = QVBoxLayout()

        self.database_manager = database_manager

        self.current_selection = QRadioButton("Export current selection from database")
        self.all_images = QRadioButton("Export all entires from database")
        self.info_classes = QLabel("Amount of classes in the exported name")
        self.current_selection.setChecked(True)
        self.num_classes = QSpinBox()
        self.num_classes.setMinimum(0)
        self.num_classes.setMaximum(10)
        self.num_classes.setValue(3)
        self.example_name_info = QLabel("Example name with current settings:")
        self.example_name = QLabel(f"{self.class_names[0]}_{self.class_names[1]}_{self.class_names[2]}-a1b2c3d4-{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.jpg")
        self.date_checkbox = QCheckBox("Timestamp?", self)
        self.date_checkbox.setChecked(True)
        self.folder = QRadioButton("Export to folder")
        self.zip = QRadioButton("Export to ZIP")
        self.folder.setChecked(True)
        

        self.selection_group = QButtonGroup()
        self.selection_group.addButton(self.current_selection,1)
        self.selection_group.addButton(self.all_images,2)

        self.export_group = QButtonGroup()
        self.export_group.addButton(self.folder,1)
        self.export_group.addButton(self.zip,2)



        self.accept_export = QPushButton("Export now")
        self.export_csv = QPushButton("Export to CSV")

        
        layout.addWidget(self.current_selection)
        layout.addWidget(self.all_images)
        layout.addWidget(self.info_classes)
        layout.addWidget(self.num_classes)
        layout.addWidget(self.example_name_info)
        layout.addWidget(self.example_name)
        layout.addWidget(self.date_checkbox)
        layout.addWidget(self.folder)
        layout.addWidget(self.zip)
        layout.addWidget(self.accept_export)
        layout.addWidget(self.export_csv)


        self.setLayout(layout)


        self.num_classes.valueChanged.connect(self.num_class_changed)
        self.accept_export.clicked.connect(self.perform_export)
        self.date_checkbox.stateChanged.connect(self.num_class_changed)

    def perform_export(self):
        selected_entry_amt = self.selection_group.checkedId()
        selected_export_type = self.export_group.checkedId()
        if selected_entry_amt == 1:
            images = self.database_manager.choose_from_db(self.state_manager.filter_yes, self.state_manager.filter_no)
        if selected_entry_amt == 2:
            filter_yes = []
            filter_no = []
            images = self.database_manager.choose_from_db(filter_yes, filter_no)

        if selected_export_type == 1:
            current_folder = QFileDialog.getExistingDirectory(self, "Select image folder")
            
        if selected_export_type == 2:
            pass


        self.close()


    def select_folder(self):
        current_folder = QFileDialog.getExistingDirectory(self, "Select export folder")
        if(current_folder == ""):
            return
        self.choosen_folder = current_folder

    def num_class_changed(self):
        amount = self.num_classes.value()
        text = ""
        if amount != 0:
            for i in range(amount):
                text += self.class_names[i]
                text += "_"

            text = text[:-1]
            text += '-'

        text += "a1b2c3d4"
        if self.date_checkbox.isChecked():
            text += "-"
            text += f"{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.jpg"
        else:
            text += ".jpg"

        self.example_name.setText(text)