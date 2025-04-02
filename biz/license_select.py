from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

from gui.internal.license_select import Ui_LicenseSelectForm


class LicenseSelect(QtWidgets.QMainWindow, Ui_LicenseSelectForm):
    signal = pyqtSignal()

    def __init__(self):
        super(LicenseSelect, self).__init__(parent=None)
        self.license_select_ui = Ui_LicenseSelectForm()
        self.license_select_ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowTitleHint)
        self.license_select_ui.pushButton_cancel.clicked.connect(self.close)
        self.license_select_ui.pushButton_conform.clicked.connect(self.emit_signal)
        self.license_select_ui.toolButton.clicked.connect(self.license_path_select)

    def get_current_text(self):
        return self.license_select_ui.lineEdit.text()

    def license_path_select(self):
        license_path = QtWidgets.QFileDialog.getOpenFileName(None, "选取License文件", './')
        self.license_select_ui.lineEdit.setText(license_path[0])

    def emit_signal(self):
        if not self.get_current_text():
            QMessageBox.warning(self, '提示信息', 'License文件路径不能为空！')

        elif self.get_current_text().split('/')[-1][-4:] != '.lic':
            QMessageBox.warning(self, '提示信息', '请选择后缀为.lic的License文件！')
        else:
            self.signal.emit()
