from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtWidgets import QMessageBox
from biz.biz_thread import GetDBConnectionThread
from gui.internal.root_login import Ui_RootLoginForm


class RootLogin(QtWidgets.QMainWindow, Ui_RootLoginForm):
    _start_get_db_connection_thread = pyqtSignal()
    signal = pyqtSignal()
    result = pyqtSignal(str)
    connect = pyqtSignal(object)

    def __init__(self):
        super(RootLogin, self).__init__(parent=None)
        self.root_login_ui = Ui_RootLoginForm()
        self.root_login_ui.setupUi(self)
        self.db_type = ''
        self.ip = ''
        self.port = ''
        self.db = ''
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowTitleHint)
        self.root_login_ui.pushButton_cancel.clicked.connect(self.close)
        self.root_login_ui.pushButton_conform.clicked.connect(self.get_connection)

        self.get_db_connection_thread = GetDBConnectionThread()
        self.get_connection_thread = QThread(self)
        self.get_db_connection_thread.moveToThread(self.get_connection_thread)
        self._start_get_db_connection_thread.connect(self.get_db_connection_thread.run)
        self.get_db_connection_thread.all.connect(self.emit_connection)
        self.get_db_connection_thread.finished.connect(self.get_connection_thread.quit)

    def get_connection(self):
        if self.get_password() == '' or self.get_user() == '':
            QMessageBox.warning(self, '提示信息', '用户名或密码不能为空！')
        else:
            if self.get_connection_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
                self.result.emit('线程仍在运行，请耐心等待...')
                return
            self.get_db_connection_thread.db_type = self.db_type
            self.get_db_connection_thread.ip = self.ip
            self.get_db_connection_thread.port = self.port
            self.get_db_connection_thread.user = self.get_user()
            if self.get_user() == 'sys':
                self.get_db_connection_thread.is_sys = True
            self.get_db_connection_thread.password = self.get_password()
            self.get_db_connection_thread.db = self.db
            self.get_connection_thread.start()
            self._start_get_db_connection_thread.emit()

    def get_password(self):
        return self.root_login_ui.lineEdit_password.text()

    def get_user(self):
        return self.root_login_ui.lineEdit_root.text()

    def set_user(self, text):
        self.root_login_ui.lineEdit_root.setText(text)

    def emit_connection(self, is_connected, msg, con):
        if is_connected:
            self.result.emit('账号连接成功！')
            self.connect.emit(con)
        else:
            QMessageBox.warning(self, '提示信息', msg)

    def set_default_user(self, db_type):
        if db_type == 'MySQL':
            self.set_user('root')
        elif db_type == 'Oracle':
            self.set_user('sys')
        else:
            self.set_user('')
