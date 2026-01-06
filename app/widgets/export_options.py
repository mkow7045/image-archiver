from common import *
from datetime import datetime
import os
import shutil
from zipfile import ZipFile
import csv

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
        self.example_name = QLabel(f"{self.class_names[0]}_{self.class_names[1]}_{self.class_names[2]}-a1b2c3d4-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpg")
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
        self.export_csv.clicked.connect(self.perform_csv_export)

    def perform_export(self):
        selected_entry_amt = self.selection_group.checkedId()
        selected_export_type = self.export_group.checkedId()
        priority_classes = self.state_manager.filter_yes
        filter_empty = False
        if selected_entry_amt == 1:
            if self.state_manager.filter_yes == [] and self.state_manager.filter_no == []:
                filter_empty = True
            images = self.database_manager.choose_from_db(self.state_manager.filter_yes, self.state_manager.filter_no)
        if selected_entry_amt == 2:
            filter_yes = []
            filter_no = []
            filter_empty = True
            images = self.database_manager.choose_from_db(filter_yes, filter_no)

        if selected_export_type == 1:
            folder_to_save = QFileDialog.getExistingDirectory(self, "Select image folder")
            if(folder_to_save == ""):
                return
            for file in images:
                classes = self.database_manager.get_classes_for_single(file)
                path = os.path.join("images",file[0])
                filename = self.make_filename(classes,file[0],priority_classes,filter_empty)
                filename = os.path.join(folder_to_save,filename)
                shutil.copy(path,filename)
            
        if selected_export_type == 2:
            save_dest, _ = QFileDialog.getSaveFileName(self, "Choose place to save","","Zip files (*.zip)")
            if(save_dest == ""):
                return
            if not save_dest.endswith(".zip"):
                save_dest += ".zip"
            file_list = []
            for file in images:
                classes = self.database_manager.get_classes_for_single(file)
                filename = self.make_filename(classes,file[0],priority_classes,filter_empty)
                path = os.path.join("images",file[0])
                if (path,filename) not in file_list:
                    file_list.append((path, filename))
                
            with ZipFile(save_dest, "w") as zipf:
                for file in file_list:
                    zipf.write(file[0], arcname=file[1])



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
            text += f"{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpg"
        else:
            text += ".jpg"

        self.example_name.setText(text)

    def make_filename(self, classes,og_hash,priority_classes,filter_empty):
        amount = self.num_classes.value()
        if amount > len(classes):
            amount = len(classes)
        text = ""
        if not filter_empty:
            i = 0
            while amount != 0 and i < len(priority_classes):
                text += priority_classes[i]
                text += "_"
                amount -= 1
                i += 1
            
            text = text[:-1]
            text += '-'

        i = 0
        while amount != 0:
            if classes[i] not in priority_classes:
                text += classes[i]
                text += "_"
                amount -= 1
                i += 1

        text = text[:-1]
        text += '-' 

        text += og_hash[:8]
        if self.date_checkbox.isChecked():
            text += "-"
            text += f"{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpg"
        else:
            text += ".jpg"

        return text
    

    def perform_csv_export(self):
        selected_entry_amt = self.selection_group.checkedId()
        priority_classes = self.state_manager.filter_yes
        filter_empty = False
        if selected_entry_amt == 1:
            if self.state_manager.filter_yes == [] and self.state_manager.filter_no == []:
                filter_empty = True
            images = self.database_manager.choose_from_db(self.state_manager.filter_yes, self.state_manager.filter_no)
        if selected_entry_amt == 2:
            filter_yes = []
            filter_no = []
            filter_empty = True
            images = self.database_manager.choose_from_db(filter_yes, filter_no)

            
        save_dest, _ = QFileDialog.getSaveFileName(self, "Choose place to save","","CSV files (*.csv)")
        if(save_dest == ""):
            return
        if not save_dest.endswith(".csv"):
            save_dest += ".csv"

        rows = self.database_manager.get_info_for_images(images)
        with open(save_dest, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            writer.writerow(['name','model_name','class_name','conf','x1','y1','x2','y2'])
            writer.writerows(rows)

        self.close()
        


            
