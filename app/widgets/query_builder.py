from common import *

class SignalCheckBox(QCheckBox):
    clicked = pyqtSignal(str)
    unclicked = pyqtSignal(str)
    def __init__(self,img_class):
        super().__init__(img_class)
        self.img_class = img_class
        self.stateChanged.connect(self.state_changed)

    def state_changed(self, state):
        if state == Qt.CheckState.Checked:
            self.clicked.emit(self.img_class)
        else:
            self.unclicked.emit(self.img_class)



class QueryBuilder(QDialog):

    def __init__(self, state_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Query Builder")
        self.setModal(True)
        self.setMinimumSize(650,300)

        layout = QVBoxLayout()
        self.area_on_layout = QVBoxLayout()
        self.area_off_layout = QVBoxLayout()

        self.state_manager = state_manager
        filter_yes_set = set()
        filter_no_set = set()

        self.sample_query = QLabel("")
        self.conf_check = QCheckBox()
        self.conf_slider = QSlider()
        self.filter_chooser = QLineEdit()
        self.filter_chooser.setPlaceholderText("Filter")
        self.checkbox_filters = QWidget()
        checkbox_filters_layout = QHBoxLayout()
        self.filters_on = QScrollArea()
        self.filters_off = QScrollArea()
        self.filters_on.setWidgetResizable(True)
        self.filters_off.setWidgetResizable(True)

        self.checkboxes_on = QWidget()
        self.checkboxes_on_layout = QVBoxLayout()
        self.checkboxes_on.setLayout(self.checkboxes_on_layout)

        self.checkboxes_off = QWidget()
        self.checkboxes_off_layout = QVBoxLayout()
        self.checkboxes_off.setLayout(self.checkboxes_off_layout)

        self.filters_on.setWidget(self.checkboxes_on)
        self.filters_off.setWidget(self.checkboxes_off)

        checkbox_filters_layout.addWidget(self.filters_on)
        checkbox_filters_layout.addWidget(self.filters_off)

        self.checkbox_filters.setLayout(checkbox_filters_layout)
        

        layout.addWidget(self.sample_query)
        layout.addWidget(self.conf_check)
        layout.addWidget(self.conf_slider)
        layout.addWidget(self.filter_chooser)
        layout.addWidget(self.checkbox_filters)

        self.fill_scroll_area(self.checkboxes_on_layout)
        self.fill_scroll_area(self.checkboxes_off_layout)

        self.setLayout(layout)

    def fill_scroll_area(self,area_layout): #is_negative,filter
        while area_layout.count():
            item = area_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        classes = self.state_manager.class_names
        for class_id, class_name in classes.items():
            checkbox = SignalCheckBox(class_name)
            area_layout.addWidget(checkbox)



        
