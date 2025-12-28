from common import *

class StateManager(QObject):
    results_changed = pyqtSignal(object)
    image_path_changed = pyqtSignal(str)
    conf_changed = pyqtSignal(float)
    class_names_changed = pyqtSignal(dict)
    model_name_changed = pyqtSignal(str)
    busy_changed = pyqtSignal(bool)


    def __init__(self):
        super().__init__()
        self._image_path = ""
        self._conf = 0.25
        self._class_names = ""
        self._model_name = ""
        self._results = ""
        self._busy = False
        self.filter_yes = []
        self.filter_no = []
        self.conf_filter = 0.0
        self.color = Qt.GlobalColor.black
        self._processing_running = False

    @property
    def image_path(self):
        return self._image_path
    
    @image_path.setter
    def image_path(self,image_path):
        if self._image_path != image_path:
            self._image_path = image_path
            self.image_path_changed.emit(image_path)

    @property
    def conf(self):
        return self._conf
    
    @conf.setter
    def conf(self,conf):
        if self._conf != conf:
            self._conf = conf
            self.conf_changed.emit(conf)

    @property
    def class_names(self):
        return self._class_names
    
    @class_names.setter
    def class_names(self,class_names):
        if self._class_names != class_names:
            self._class_names = class_names
            self.class_names_changed.emit(class_names)

    @property
    def model_name(self):
        return self._model_name
    
    @model_name.setter
    def model_name(self,model_name):
        if self._model_name != model_name:
            self._model_name = model_name
            self.model_name_changed.emit(model_name)

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self,results):
        self._results = results
        self.results_changed.emit(results)

    @property
    def busy(self):
        return self._busy

    @busy.setter
    def busy(self,busy):
        self._busy = busy
        self.busy_changed.emit(busy)

    @property
    def processing_running(self):
        return self._processing_running

    @processing_running.setter
    def processing_running(self,processing_running):
        self._processing_running = processing_running



