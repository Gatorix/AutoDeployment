from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

from gui.internal.save_db_config import Ui_SaveDbConfigForm


class SaveDbConfig(QtWidgets.QMainWindow, Ui_SaveDbConfigForm):
    signal = pyqtSignal()
    result = pyqtSignal(str)

    def __init__(self):
        super(SaveDbConfig, self).__init__(parent=None)
        self.save_db_config_ui = Ui_SaveDbConfigForm()
        self.save_db_config_ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowTitleHint)
        self.save_db_config_ui.pushButton_cancel.clicked.connect(self.close)
        self.save_db_config_ui.pushButton_conform.clicked.connect(self.emit_signal)

    def set_default_text(self, text):
        self.save_db_config_ui.lineEdit_config_name.setText(text)

    def get_current_text(self):
        return self.save_db_config_ui.lineEdit_config_name.text()

    def emit_signal(self):
        if self.get_current_text():
            self.signal.emit()
        else:
            QMessageBox.warning(self, '提示信息', '配置名称不能为空！')
