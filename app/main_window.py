from common import *
from .pages.main_page import MainPage



class MainWindow(QMainWindow):
    def __init__(self,width,height,state_manager,database_manager):
        super().__init__()
        self.setWindowTitle("Detector App")
        window_width = int(width*0.6)
        window_height = int(width*0.4)
        self.setGeometry(int((width-window_width)/2),int((height - window_height)/2),window_width,window_height)

        self.main_page = MainPage(state_manager,database_manager)
        self.setCentralWidget(self.main_page)

    
