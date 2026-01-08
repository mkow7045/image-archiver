from common import *

class BaseDetector(QObject):
    def __init__(self,model_name):
        super().__init__()
        self.model_name = model_name