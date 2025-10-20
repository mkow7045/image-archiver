from common import *

class BaseDetector(QObject):
    def __init__(self,model_name, conf):
        super().__init__()
        self.conf = conf
        self.model_name = model_name