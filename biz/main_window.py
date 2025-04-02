from PyQt6 import QtWidgets, QtCore, sip, QtGui
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QMessageBox, QMenu, QTabBar, QTextBrowser
from gui.internal.one_click import Ui_OneClick
from biz.save_db_config import SaveDbConfig
from biz.license_select import LicenseSelect
from biz.root_login import RootLogin
from biz.db.run_sql import mysql_run_sql, oracle_run_sql, query_sql
from biz.file.check import check_path
from biz.file.modify import modify_file
from biz.file.config import save_config, save_db_config, read_yaml, write_yaml, clear_yaml, get_current_path, \
    save_bank_config, get_bank_info
from biz.file.file_path import get_all_filepath, is_dir, copy_file, get_sys_env_path, remove_temp_tree, check_license, \
    get_encoding, is_file
from utils.str_func import check_url, check_structure_name, check_patch_name, convert_slash
from utils.cmd import check_service, kill_process
from biz.biz_thread import MysqlInitThread, StartMysqlThread, CheckDBConnectionThread, GetDBConnectionThread, \
    RunInitSqlThread, GetStructureThread, UpdateStructureThread, GetPatchThread, UpdatePatchThread, StartT2Thread, \
    PortCheckThread, StartOracleThread, TomcatMonitorThread, LogPrintThread, BankUpdateThread, UnzipWarPackageThread


class MainWindow(QtWidgets.QMainWindow, Ui_OneClick):
    _start_mysql_init_thread = pyqtSignal()
    _start_mysql_server_thread = pyqtSignal()
    _start_oracle_server_thread = pyqtSignal()
    _start_check_db_connection_thread = pyqtSignal()
    _start_check_be_db_connection_thread = pyqtSignal()
    _start_get_db_connection_thread = pyqtSignal()
    _start_get_init_db_connection_thread = pyqtSignal()
    _start_get_run_sql_db_connection_thread = pyqtSignal()
    _start_run_init_sql_thread = pyqtSignal()
    _start_get_structure_thread = pyqtSignal()
    _start_update_structure_thread = pyqtSignal()
    _start_get_patch_thread = pyqtSignal()
    _start_update_patch_thread = pyqtSignal()
    _start_t2_thread = pyqtSignal()
    _start_port_check_thread = pyqtSignal()
    _start_log_monitor_thread = pyqtSignal()
    _start_biz_1_monitor_thread = pyqtSignal()
    _start_biz_2_monitor_thread = pyqtSignal()
    _start_biz_3_monitor_thread = pyqtSignal()
    _start_db_log_print_thread = pyqtSignal()
    _start_update_log_print_thread = pyqtSignal()
    _start_biz_1_log_print_thread = pyqtSignal()
    _start_biz_2_log_print_thread = pyqtSignal()
    _start_biz_3_log_print_thread = pyqtSignal()
    _start_bank_update_thread = pyqtSignal()
    _start_unzip_war_package_thread = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__(parent=None)
        self.mysql_init_thread = MysqlInitThread()  # 创建线程对象
        self.start_mysql_server_thread = StartMysqlThread()
        self.start_oracle_server_thread = StartOracleThread()
        self.check_db_connection_thread = CheckDBConnectionThread()
        self.check_be_db_connection_thread = CheckDBConnectionThread()
        self.get_db_connection_thread = GetDBConnectionThread()
        self.get_init_db_connection_thread = GetDBConnectionThread()
        self.get_run_sql_db_connection_thread = GetDBConnectionThread()
        self.run_init_sql_thread = RunInitSqlThread()
        self.get_structure_thread = GetStructureThread()
        self.update_structure_thread = UpdateStructureThread()
        self.get_patch_thread = GetPatchThread()
        self.update_patch_thread = UpdatePatchThread()
        self.start_t2_thread = StartT2Thread()
        self.port_check_thread = PortCheckThread()
        self.log_monitor_thread = TomcatMonitorThread()
        self.log_biz_1_monitor_thread = TomcatMonitorThread()
        self.log_biz_2_monitor_thread = TomcatMonitorThread()
        self.log_biz_3_monitor_thread = TomcatMonitorThread()
        self.log_db_print_thread = LogPrintThread()
        self.log_update_print_thread = LogPrintThread()
        self.log_biz_1_print_thread = LogPrintThread()
        self.log_biz_2_print_thread = LogPrintThread()
        self.log_biz_3_print_thread = LogPrintThread()
        self.bank_update_thread = BankUpdateThread()
        self.unzip_war_package_thread = UnzipWarPackageThread()

        self.init_thread = QThread(self)  # 初始化QThread子线程
        self.server_thread = QThread(self)
        self.oracle_server_thread = QThread(self)
        self.check_connection_thread = QThread(self)
        self.check_be_connection_thread = QThread(self)
        self.get_connection_thread = QThread(self)
        self.get_init_connection_thread = QThread(self)
        self.get_run_sql_connection_thread = QThread(self)
        self.run_sql_thread = QThread(self)
        self.structure_thread = QThread(self)
        self.update_structure_main_thread = QThread(self)
        self.patch_thread = QThread(self)
        self.update_patch_main_thread = QThread(self)
        self.start_t2_main_thread = QThread(self)
        self.port_check_main_thread = QThread(self)
        self.log_monitor_main_thread = QThread(self)
        self.log_biz_1_monitor_main_thread = QThread(self)
        self.log_biz_2_monitor_main_thread = QThread(self)
        self.log_biz_3_monitor_main_thread = QThread(self)
        self.log_db_print_main_thread = QThread(self)
        self.log_update_print_main_thread = QThread(self)
        self.log_biz_1_print_main_thread = QThread(self)
        self.log_biz_2_print_main_thread = QThread(self)
        self.log_biz_3_print_main_thread = QThread(self)
        self.bank_update_main_thread = QThread(self)
        self.unzip_war_package_main_thread = QThread(self)

        self.unzip_war_package_thread.moveToThread(self.unzip_war_package_main_thread)
        self._start_unzip_war_package_thread.connect(self.unzip_war_package_thread.run)
        self.unzip_war_package_thread.signal.connect(self.print_to_be_text_browser)
        self.unzip_war_package_thread.finished.connect(self.unzip_war_package_main_thread.quit)

        self.bank_update_thread.moveToThread(self.bank_update_main_thread)
        self._start_bank_update_thread.connect(self.bank_update_thread.run)
        self.bank_update_thread.signal.connect(self.print_to_be_text_browser)
        self.bank_update_thread.finished.connect(self.bank_update_main_thread.quit)

        self.log_db_print_thread.moveToThread(self.log_db_print_main_thread)
        self._start_db_log_print_thread.connect(self.log_db_print_thread.run)
        self.log_db_print_thread.signal.connect(self.print_to_new_text_browser)
        self.log_db_print_thread.finished.connect(self.log_db_print_main_thread.quit)

        self.log_update_print_thread.moveToThread(self.log_update_print_main_thread)
        self._start_update_log_print_thread.connect(self.log_update_print_thread.run)
        self.log_update_print_thread.signal.connect(self.print_to_new_text_browser)
        self.log_update_print_thread.finished.connect(self.log_update_print_main_thread.quit)

        self.log_biz_1_print_thread.moveToThread(self.log_biz_1_print_main_thread)
        self._start_biz_1_log_print_thread.connect(self.log_biz_1_print_thread.run)
        self.log_biz_1_print_thread.signal.connect(self.print_to_new_text_browser)
        self.log_biz_1_print_thread.finished.connect(self.log_biz_1_print_main_thread.quit)

        self.log_biz_2_print_thread.moveToThread(self.log_biz_2_print_main_thread)
        self._start_biz_2_log_print_thread.connect(self.log_biz_2_print_thread.run)
        self.log_biz_2_print_thread.signal.connect(self.print_to_new_text_browser)
        self.log_biz_2_print_thread.finished.connect(self.log_biz_2_print_main_thread.quit)

        self.log_biz_3_print_thread.moveToThread(self.log_biz_3_print_main_thread)
        self._start_biz_3_log_print_thread.connect(self.log_biz_3_print_thread.run)
        self.log_biz_3_print_thread.signal.connect(self.print_to_new_text_browser)
        self.log_biz_3_print_thread.finished.connect(self.log_biz_3_print_main_thread.quit)

        self.log_monitor_thread.moveToThread(self.log_monitor_main_thread)
        self._start_log_monitor_thread.connect(self.log_monitor_thread.run)
        self.log_monitor_thread.update_started.connect(self.update_log_printer_starter)
        self.log_monitor_thread.signal.connect(self.print_to_te_text_browser)
        self.log_monitor_thread.finished.connect(self.log_monitor_main_thread.quit)
        self.log_monitor_thread.finished.connect(self.log_monitor_thread.reset_thread)

        self.log_biz_1_monitor_thread.moveToThread(self.log_biz_1_monitor_main_thread)
        self._start_biz_1_monitor_thread.connect(self.log_biz_1_monitor_thread.run)
        self.log_biz_1_monitor_thread.biz_1_started.connect(self.biz_1_log_printer_starter)
        self.log_biz_1_monitor_thread.signal.connect(self.print_to_te_text_browser)
        self.log_biz_1_monitor_thread.finished.connect(self.log_biz_1_monitor_main_thread.quit)

        self.log_biz_2_monitor_thread.moveToThread(self.log_biz_2_monitor_main_thread)
        self._start_biz_2_monitor_thread.connect(self.log_biz_2_monitor_thread.run)
        self.log_biz_2_monitor_thread.biz_2_started.connect(self.biz_2_log_printer_starter)
        self.log_biz_2_monitor_thread.signal.connect(self.print_to_te_text_browser)
        self.log_biz_2_monitor_thread.finished.connect(self.log_biz_2_monitor_main_thread.quit)

        self.log_biz_3_monitor_thread.moveToThread(self.log_biz_3_monitor_main_thread)
        self._start_biz_3_monitor_thread.connect(self.log_biz_3_monitor_thread.run)
        self.log_biz_3_monitor_thread.biz_3_started.connect(self.biz_3_log_printer_starter)
        self.log_biz_3_monitor_thread.signal.connect(self.print_to_te_text_browser)
        self.log_biz_3_monitor_thread.finished.connect(self.log_biz_3_monitor_main_thread.quit)

        self.port_check_thread.moveToThread(self.port_check_main_thread)
        self._start_port_check_thread.connect(self.port_check_thread.run)
        self.port_check_thread.signal.connect(self.print_to_te_text_browser)
        self.port_check_thread.is_biz_port_tested.connect(self.te_modify)
        self.port_check_thread.is_update_port_tested.connect(self.update_patch_pre)
        self.port_check_thread.finished.connect(self.port_check_main_thread.quit)

        self.start_t2_thread.moveToThread(self.start_t2_main_thread)
        self._start_t2_thread.connect(self.start_t2_thread.run)
        self.start_t2_thread.started.connect(self.biz_log_monitor)
        self.start_t2_thread.signal.connect(self.print_to_te_text_browser)
        self.start_t2_thread.finished.connect(self.start_t2_main_thread.quit)

        self.mysql_init_thread.moveToThread(self.init_thread)
        self._start_mysql_init_thread.connect(self.mysql_init_thread.run)  # 只能通过信号-槽启动线程处理函数
        self.mysql_init_thread.started.connect(self.lock_te_db_config_input)
        self.mysql_init_thread.signal.connect(self.print_to_te_text_browser)
        self.mysql_init_thread.user.connect(self.set_te_db_user)
        self.mysql_init_thread.password.connect(self.set_te_db_password)
        self.mysql_init_thread.finished.connect(self.init_thread.quit)
        self.mysql_init_thread.next_step.connect(self.get_init_db_connection)
        self.mysql_init_thread.finished.connect(self.unlock_te_db_config_input)

        self.start_mysql_server_thread.moveToThread(self.server_thread)
        self._start_mysql_server_thread.connect(self.start_mysql_server_thread.run)
        self.start_mysql_server_thread.started.connect(self.lock_te_db_config_input)
        self.start_mysql_server_thread.signal.connect(self.print_to_te_text_browser)
        self.start_mysql_server_thread.finished.connect(self.unlock_te_db_config_input)
        self.start_mysql_server_thread.finished.connect(self.server_thread.quit)
        # self.start_mysql_server_thread.finished.connect(self.recheck_server)

        self.start_oracle_server_thread.moveToThread(self.oracle_server_thread)
        self._start_oracle_server_thread.connect(self.start_oracle_server_thread.run)
        self.start_oracle_server_thread.started.connect(self.lock_te_db_config_input)
        self.start_oracle_server_thread.signal.connect(self.print_to_te_text_browser)
        self.start_oracle_server_thread.finished.connect(self.unlock_te_db_config_input)
        self.start_oracle_server_thread.finished.connect(self.oracle_server_thread.quit)
        # self.start_oracle_server_thread.finished.connect(self.recheck_server)

        self.check_db_connection_thread.moveToThread(self.check_connection_thread)
        self._start_check_db_connection_thread.connect(self.check_db_connection_thread.run)
        self.check_db_connection_thread.started.connect(self.lock_te_db_config_input)
        self.check_db_connection_thread.signal.connect(self.print_to_te_text_browser)
        self.check_db_connection_thread.result.connect(self.set_db_test_flag)
        self.check_db_connection_thread.init_result.connect(self.show_root_login)
        self.check_db_connection_thread.config.connect(self.set_db_tested_config)
        self.check_db_connection_thread.finished.connect(self.check_connection_thread.quit)
        self.check_db_connection_thread.finished.connect(self.unlock_te_db_config_input)

        self.check_be_db_connection_thread.moveToThread(self.check_be_connection_thread)
        self._start_check_be_db_connection_thread.connect(self.check_be_db_connection_thread.run)
        self.check_be_db_connection_thread.started.connect(self.lock_be_db_config_input)
        self.check_be_db_connection_thread.signal.connect(self.print_to_be_text_browser)
        self.check_be_db_connection_thread.result.connect(self.set_be_db_test_flag)
        self.check_be_db_connection_thread.config.connect(self.set_be_db_tested_config)
        self.check_be_db_connection_thread.finished.connect(self.check_be_connection_thread.quit)
        self.check_be_db_connection_thread.finished.connect(self.unlock_be_db_config_input)

        self.get_db_connection_thread.moveToThread(self.get_connection_thread)
        self._start_get_db_connection_thread.connect(self.get_db_connection_thread.run)
        self.get_db_connection_thread.started.connect(self.lock_te_db_config_input)
        self.get_db_connection_thread.signal.connect(self.print_to_te_text_browser)
        self.get_db_connection_thread.connect.connect(self.is_inited)
        self.get_db_connection_thread.result.connect(self.set_db_test_flag)
        self.get_db_connection_thread.config.connect(self.set_db_tested_config)
        self.get_db_connection_thread.finished.connect(self.get_connection_thread.quit)
        self.get_db_connection_thread.finished.connect(self.unlock_te_db_config_input)

        self.get_init_db_connection_thread.moveToThread(self.get_init_connection_thread)
        self._start_get_init_db_connection_thread.connect(self.get_init_db_connection_thread.run)
        self.get_init_db_connection_thread.started.connect(self.lock_te_db_config_input)
        self.get_init_db_connection_thread.signal.connect(self.print_to_te_text_browser)
        self.get_init_db_connection_thread.connect.connect(self.create_user_and_database)
        self.get_init_db_connection_thread.result.connect(self.set_db_test_flag)
        self.get_init_db_connection_thread.config.connect(self.set_db_tested_config)
        self.get_init_db_connection_thread.finished.connect(self.get_init_connection_thread.quit)
        self.get_init_db_connection_thread.finished.connect(self.unlock_te_db_config_input)

        self.get_run_sql_db_connection_thread.moveToThread(self.get_run_sql_connection_thread)
        self._start_get_run_sql_db_connection_thread.connect(self.get_run_sql_db_connection_thread.run)
        self.get_run_sql_db_connection_thread.started.connect(self.lock_te_db_config_input)
        self.get_run_sql_db_connection_thread.signal.connect(self.print_to_te_text_browser)
        self.get_run_sql_db_connection_thread.connect.connect(self.is_inited)
        self.get_run_sql_db_connection_thread.result.connect(self.set_db_test_flag)
        self.get_run_sql_db_connection_thread.config.connect(self.set_db_tested_config)
        self.get_run_sql_db_connection_thread.finished.connect(self.get_run_sql_connection_thread.quit)
        self.get_run_sql_db_connection_thread.finished.connect(self.unlock_te_db_config_input)

        self.run_init_sql_thread.moveToThread(self.run_sql_thread)
        self._start_run_init_sql_thread.connect(self.run_init_sql_thread.run)
        self.run_init_sql_thread.started.connect(self.lock_te_db_config_input)
        self.run_init_sql_thread.signal.connect(self.print_to_te_text_browser)
        self.run_init_sql_thread.finished.connect(self.run_sql_thread.quit)
        self.run_init_sql_thread.finished.connect(self.unlock_te_db_config_input)

        self.get_structure_thread.moveToThread(self.structure_thread)
        self._start_get_structure_thread.connect(self.get_structure_thread.run)
        self.get_structure_thread.signal.connect(self.print_to_te_text_browser)
        self.get_structure_thread.finished.connect(self.structure_thread.quit)
        self.get_structure_thread.finished.connect(self.update_structure_main)

        self.update_structure_thread.moveToThread(self.update_structure_main_thread)
        self._start_update_structure_thread.connect(self.update_structure_thread.run)
        self.update_structure_thread.signal.connect(self.print_to_te_text_browser)
        self.update_structure_thread.finished.connect(self.update_structure_main_thread.quit)

        self.get_patch_thread.moveToThread(self.patch_thread)
        self._start_get_patch_thread.connect(self.get_patch_thread.run)
        self.get_patch_thread.signal.connect(self.print_to_te_text_browser)
        self.get_patch_thread.finished.connect(self.patch_thread.quit)
        self.get_patch_thread.finished.connect(self.update_patch_main)

        self.update_patch_thread.moveToThread(self.update_patch_main_thread)
        self._start_update_patch_thread.connect(self.update_patch_thread.run)
        self.update_patch_thread.start_monitoring.connect(self.update_log_monitor)
        self.update_patch_thread.signal.connect(self.print_to_te_text_browser)
        self.update_patch_thread.finished.connect(self.update_patch_main_thread.quit)

        # self.thread.started.connect(self.worker.run)
        # self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)

        self.ui = Ui_OneClick()
        remove_temp_tree()
        self.child_save_db_config = SaveDbConfig()
        self.child_save_db_config.signal.connect(self.save_te_db_config_to_yml)
        self.child_save_db_config.result.connect(self.print_to_te_text_browser)

        self.child_be_save_db_config = SaveDbConfig()
        self.child_be_save_db_config.signal.connect(self.save_be_db_config_to_yml)
        self.child_be_save_db_config.result.connect(self.print_to_be_text_browser)

        self.child_root_login = RootLogin()
        self.child_root_login.result.connect(self.print_to_te_text_browser)
        self.child_root_login.connect.connect(self.create_user_and_database)

        self.child_license_select = LicenseSelect()
        self.child_license_select.signal.connect(self.copy_license_file)

        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./data/resource/favicon_256.ico'))

        self.is_te_db_tested = False
        self.is_be_db_tested = False
        self.is_te_env_configured = False
        self.is_be_env_configured = False
        self.is_te_biz_port_tested = False
        self.is_te_update_port_tested = False

        self.current_te_db_config = []
        self.tested_te_db_config = []

        self.current_be_db_config = []
        self.tested_be_db_config = []

        self.current_te_path_config = []
        self.configured_te_path_config = []

        self.current_be_path_config = []
        self.configured_be_path_config = []

        self.tested_biz_port = ''
        self.tested_update_port = ''

        self.load_saved_db_config()
        self.load_saved_bank_config()
        self.set_config()
        self.bank_info = get_bank_info()
        self.ui.comboBox_be_bank_type.addItems([*self.bank_info])
        self.already_get_this_bank = ''
        self.current_bank_front_config_labels = []
        self.current_bank_front_config_line_edits = []
        self.switch_current_bank_version()

        self.opened_tab_obj_name = []
        self.opened_text_browser_obj_name = []

        self.started_tomcat_port = []

        self.thread_tab_mapping = {}

        self.properties_keys = []
        self.properties_values = []

        self.is_license_configured = False

        # t2_environment path select actions
        self.ui.toolButton_te_program_path_selecter.clicked.connect(self.select_te_program_path)
        self.ui.toolButton_te_update_path_selecter.clicked.connect(self.select_te_update_path)
        self.ui.toolButton_te_tomcat_path_selecter.clicked.connect(self.select_te_tomcat_path)
        # self.ui.toolButton_te_jdk_path_selecter.clicked.connect(self.select_te_jdk_path)
        self.ui.toolButton_te_structure_path_selecter.clicked.connect(self.select_te_structure_path)
        self.ui.toolButton_te_patch_path_selecter.clicked.connect(self.select_te_patch_path)
        self.ui.pushButton_te_db_save_current_config.clicked.connect(self.check_te_db_config)
        self.ui.comboBox_te_db_config_name.activated.connect(self.switch_current_db_config)

        self.ui.pushButton_te_db_test.clicked.connect(self.check_te_db_connection)
        # get jdk path in system environment
        # self.ui.pushButton_te_get_sys_jdk_path.clicked.connect(self.get_te_sys_jdk_path)
        # init database action
        # self.ui.pushButton_te_install_mysql.clicked.connect(self.database_init)
        self.ui.pushButton_te_install_mysql.clicked.connect(self.database_init)
        # path config
        # self.ui.pushButton_te_path_config.clicked.connect(self.te_path_config)
        # self.ui.pushButton_te_pro_path_config.clicked.connect(self.testlog)
        # self.ui.pushButton_te_pro_path_config.setEnabled(False)
        # self.ui.pushButton_te_port_check.clicked.connect(self.port_check)

        self.ui.pushButton_te_update_structure.clicked.connect(self.update_structure)
        self.ui.pushButton_te_start_update.clicked.connect(self.update_patch)
        # self.ui.pushButton_te_start_update.clicked.connect()
        self.ui.pushButton_te_start_t2.clicked.connect(self.te_path_config)

        # textBrowser右键菜单
        self.ui.textBrowser_te_logs.customContextMenuRequested[QtCore.QPoint].connect(self.log_right_click_menu)
        self.ui.textBrowser_be_logs.customContextMenuRequested[QtCore.QPoint].connect(self.be_log_right_click_menu)
        # 保存当前配置右键菜单
        self.ui.pushButton_te_db_save_current_config.customContextMenuRequested[QtCore.QPoint].connect(
            self.save_config_right_click_menu)
        self.ui.pushButton_be_db_save_current_config.customContextMenuRequested[QtCore.QPoint].connect(
            self.save_be_config_right_click_menu)
        # 启动升级工具按钮右键菜单
        self.ui.pushButton_te_start_update.customContextMenuRequested[QtCore.QPoint].connect(
            self.start_update_right_click_menu)
        # 启动业务系统按钮右键菜单
        self.ui.pushButton_te_start_t2.customContextMenuRequested[QtCore.QPoint].connect(
            self.start_t2_right_click_menu)
        # 启动redis按钮右键菜单
        self.ui.pushButton_be_start_redis.customContextMenuRequested[QtCore.QPoint].connect(
            self.start_redis_right_click_menu)
        # 启动客户端按钮右键菜单
        self.ui.pushButton_be_start_client.customContextMenuRequested[QtCore.QPoint].connect(
            self.start_client_right_click_menu)
        # 启动服务端按钮右键菜单
        self.ui.pushButton_be_start_server.customContextMenuRequested[QtCore.QPoint].connect(
            self.start_server_right_click_menu)
        # 日志框配置
        self.ui.tabWidget_te_log.setTabsClosable(True)
        self.ui.tabWidget_te_log.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)
        self.ui.tabWidget_te_log.tabCloseRequested.connect(self.close_tab)
        self.ui.tabWidget_be_log.setTabsClosable(True)
        self.ui.tabWidget_be_log.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)
        self.ui.tabWidget_be_log.tabCloseRequested.connect(self.close_tab)
        # bank_environment path select actions
        self.ui.toolButton_be_redis_path_selecter.clicked.connect(self.select_be_redis_path)
        self.ui.toolButton_be_server_path_selecter.clicked.connect(self.select_be_server_path)
        self.ui.toolButton_be_client_path_selecter.clicked.connect(self.select_be_client_path)
        self.ui.toolButton_be_logs_path_selecter.clicked.connect(self.select_be_logs_path)
        self.ui.toolButton_be_war_path_selecter.clicked.connect(self.select_be_war_path)

        # test db connection
        self.ui.pushButton_be_db_test.clicked.connect(self.check_be_db_connection)
        self.ui.pushButton_be_db_save_current_config.clicked.connect(self.check_be_db_config)
        self.ui.comboBox_be_db_config_name.activated.connect(self.switch_current_bank_config)
        self.ui.comboBox_be_bank_type.activated.connect(self.switch_current_bank_version)
        self.ui.pushButton_be_run_update_sql.clicked.connect(self.run_bank_update_sql)
        # self.ui.pushButton_get_bank_front_config.clicked.connect(self.create_bank_front_config_details)
        self.ui.pushButton_save_bank_front_config.clicked.connect(self.save_current_bank_front_config)
        self.ui.pushButton_unzip_war_package.clicked.connect(self.unzip_war_package)
        self.ui.pushButton_be_start_redis.clicked.connect(self.start_redis)
        self.ui.pushButton_be_start_server.clicked.connect(self.start_server)
        self.ui.pushButton_be_start_client.clicked.connect(self.start_client)

    def start_redis(self):
        pass

    def start_server(self):
        pass

    def start_client(self):
        pass

    def unzip_war_package(self):
        if not self.get_be_war_path():
            self.print_to_be_text_browser('请输入War包路径！')
        elif not self.get_be_client_path():
            self.print_to_be_text_browser('请输入客户端路径！')
        elif not self.get_be_server_path():
            self.print_to_be_text_browser('请输入服务端路径！')
        else:
            if self.unzip_war_package_main_thread.isRunning():
                self.print_to_be_text_browser('线程仍在运行，请耐心等待...')
                return
            self.unzip_war_package_thread.war_path = self.get_be_war_path()
            self.unzip_war_package_thread.client_path = self.get_be_client_path()
            self.unzip_war_package_thread.server_path = self.get_be_server_path()
            self.unzip_war_package_main_thread.start()
            self._start_unzip_war_package_thread.emit()

    @staticmethod
    def restore_properties(config_file_path, properties_keys, properties_values):
        with open(config_file_path, 'w', encoding=get_encoding(config_file_path)) as properties:
            properties.truncate(0)
            for i in range(len(properties_keys)):
                properties.write('%s=%s' % (
                    properties_keys[i],
                    properties_values[i]))

    def save_current_bank_front_config(self):
        pre_properties_keys, pre_properties_values = self.get_bank_front_config_details()
        properties_keys, properties_values = self.get_bank_front_config_details()
        config_file_path = '%s/webapps/bank/WEB-INF/classes/conf/%s' % (self.get_be_client_path(),
                                                                        self.ui.lineEdit_be_bank_config.text())
        if is_file(config_file_path):
            try:
                with open(config_file_path, 'w', encoding=get_encoding(config_file_path)) as properties:
                    properties.truncate(0)
                    for _ in properties_keys:
                        properties.write('%s=%s\n' % (
                            _,
                            self.ui.groupBox_bank_front_config.findChild(QtWidgets.QLineEdit,
                                                                         "lineEdit_%s" % _).text()))
                self.print_to_be_text_browser('前置机配置保存成功！')
            except UnicodeDecodeError:
                self.print_to_be_text_browser(
                    '配置文件解析错误，请检查%s文件编码格式，并手动修改后重试！\n文件路径：%s' %
                    (config_file_path.split('/')[-1], config_file_path))
                self.restore_properties(config_file_path, pre_properties_keys, pre_properties_values)
                return
            except UnicodeEncodeError as uee:
                self.print_to_be_text_browser('配置文件保存失败，编码错误！\n%s' % uee)
                self.restore_properties(config_file_path, pre_properties_keys, pre_properties_values)
                return
            except AttributeError:
                self.print_to_be_text_browser('配置文件保存失败，元素不存在！')
                self.restore_properties(config_file_path, pre_properties_keys, pre_properties_values)
                return

    def get_bank_front_config_details(self):
        if not self.get_be_client_path():
            self.print_to_be_text_browser('请输入客户端路径！')
        else:
            properties_keys = []
            properties_values = []
            config_file_path = '%s/webapps/bank/WEB-INF/classes/conf/%s' % (self.get_be_client_path(),
                                                                            self.ui.lineEdit_be_bank_config.text())
            if is_file(config_file_path):
                try:
                    with open(config_file_path, 'r', encoding=get_encoding(config_file_path)) as properties:
                        for line in properties:
                            if not line.startswith('#'):
                                if line.split('=')[0] not in properties_keys:
                                    properties_keys.append(line.split('=')[0])
                                    properties_values.append(line.split('=')[1])
                except IndexError:
                    self.print_to_be_text_browser(
                        '配置文件解析错误，请检查%s文件中是否存在以"\\\\"或其他转义字符结尾的行或连续空行，并手动修改后重试！\n文件路径：%s' %
                        (config_file_path.split('/')[-1], config_file_path))
                    properties.close()
                    return
                except UnicodeDecodeError:
                    self.print_to_be_text_browser(
                        '配置文件解析错误，请检查%s文件编码格式，并手动修改后重试！\n文件路径：%s' %
                        (config_file_path.split('/')[-1], config_file_path))
                    properties.close()
                    return
                properties.close()
                return properties_keys, properties_values
            else:
                self.print_to_be_text_browser('配置文件不存在，请输入正确的客户端路径或先解压War包！')

    def create_bank_front_config_details(self):
        if self.get_current_bank_type_item() != self.already_get_this_bank:
            try:
                properties_keys, properties_values = self.get_bank_front_config_details()
                # properties_keys += properties_keys*2
                # properties_values += properties_values*2
                index = 0
                for key in properties_keys:
                    self.label = QtWidgets.QLabel(self.ui.layoutWidget7)
                    self.label.setText('%s：' % key if len(key) < 12 else '%s...：' % key[:10])
                    self.label.setObjectName("label_%s" % key)
                    self.current_bank_front_config_labels.append("label_%s" % key)
                    self.label.setToolTip(key)
                    self.ui.gridLayout_8.addWidget(self.label, 2 + index, 0, 1, 1)
                    self.line_edit = QtWidgets.QLineEdit(self.ui.layoutWidget7)
                    self.line_edit.setText(properties_values[index].replace('\n', ''))
                    self.line_edit.setObjectName("lineEdit_%s" % key)
                    self.current_bank_front_config_line_edits.append("lineEdit_%s" % key)
                    self.line_edit.setToolTip(properties_values[index].replace('\n', ''))
                    self.ui.gridLayout_8.addWidget(self.line_edit, 2 + index, 1, 1, 1)
                    index += 1
                self.already_get_this_bank = self.get_current_bank_type_item()
            except TypeError:
                # self.print_to_be_text_browser('请输入正确的客户端路径！')
                pass
        else:
            # self.already_get_this_bank = ''
            pass

    def switch_current_bank_version(self):
        self.already_get_this_bank = ''
        self.ui.lineEdit_be_bank_config.setText(
            '%s.properties' % self.bank_info[self.ui.comboBox_be_bank_type.currentText()])
        for _ in range(len(self.current_bank_front_config_labels)):
            self.ui.groupBox_bank_front_config.findChild(
                QtWidgets.QLabel, self.current_bank_front_config_labels[_]).setText('')
            self.ui.groupBox_bank_front_config.findChild(
                QtWidgets.QLabel, self.current_bank_front_config_labels[_]).setToolTip('')
            self.ui.groupBox_bank_front_config.findChild(
                QtWidgets.QLabel, self.current_bank_front_config_labels[_]).setObjectName('defaults')
            sip.delete(
                self.ui.groupBox_bank_front_config.findChild(
                    QtWidgets.QLineEdit, self.current_bank_front_config_line_edits[_]))
        self.current_bank_front_config_labels.clear()
        self.current_bank_front_config_line_edits.clear()
        self.create_bank_front_config_details()

    def run_bank_update_sql(self):
        self.save_be_db_config(self.current_be_db_config)
        if self.is_be_db_tested:
            if self.check_be_db_config_diff(self.tested_be_db_config, self.current_be_db_config):
                if self.bank_update_main_thread.isRunning():
                    self.print_to_be_text_browser('线程仍在运行，请耐心等待...')
                    return
                else:
                    self.print_to_be_text_browser('开始执行升级...')
                    self.bank_update_thread.db_type = self.get_be_db_type()
                    self.bank_update_thread.ip = self.get_be_db_ip().split(':')[0]
                    self.bank_update_thread.port = self.get_be_db_ip().split(':')[-1]
                    self.bank_update_thread.user = self.get_be_db_user()
                    self.bank_update_thread.password = self.get_be_db_password()
                    self.bank_update_thread.db = self.get_be_db_name()
                    self.bank_update_thread.is_db_tested = self.is_be_db_tested
                    self.bank_update_main_thread.start()
                    self._start_bank_update_thread.emit()
            else:
                self.print_to_be_text_browser('检测到数据库配置信息改变，请重新执行数据库连接测试！')
        else:
            self.print_to_be_text_browser('请先执行数据库连接测试！')

    def reset_update_log_monitor(self):
        self.log_monitor_thread.is_stop = True

    def new_update_log_tab(self):
        if self.ui.tabWidget_te_log.findChild(QtWidgets.QWidget, 'update'):
            QMessageBox.warning(self, '提示信息', '升级工具Tomcat已启动监控，请关闭后重试！')
            return
        # 动态创建tab
        tab = QtWidgets.QWidget()
        self.ui.tabWidget_te_log.addTab(tab, '升级工具Tomcat日志')
        tab.setObjectName('update')
        # 动态创建tab中的文本框，赋予位置、对象名称、自定义菜单等属性
        textBrowser_te_logs_new = QtWidgets.QTextBrowser(tab)
        textBrowser_te_logs_new.setGeometry(QtCore.QRect(9, 9, 1027, 375))
        textBrowser_te_logs_new.setObjectName('text_browser_update')
        textBrowser_te_logs_new.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        textBrowser_te_logs_new.customContextMenuRequested[QtCore.QPoint].connect(self.log_right_click_menu)
        # tab创建后自动打开
        self.ui.tabWidget_te_log.setCurrentWidget(tab)
        self.opened_tab_obj_name.append('update')
        self.opened_text_browser_obj_name.append('text_browser_update')

    def new_log_tab(self):
        if self.ui.tabWidget_te_log.findChild(QtWidgets.QWidget, self.get_current_db_config_item()):
            QMessageBox.warning(self, '提示信息', '当前环境Tomcat已启动监控，请关闭后重试！')
            return
        # 动态创建tab
        tab = QtWidgets.QWidget()
        self.ui.tabWidget_te_log.addTab(tab, '%s 业务系统日志' % self.get_current_db_config_item())
        tab.setObjectName(self.get_current_db_config_item())
        # 动态创建tab中的文本框，赋予位置、对象名称、自定义菜单等属性
        textBrowser_te_logs_new = QtWidgets.QTextBrowser(tab)
        textBrowser_te_logs_new.setGeometry(QtCore.QRect(9, 9, 1027, 375))
        textBrowser_te_logs_new.setObjectName('text_browser_%s' % self.get_current_db_config_item())
        textBrowser_te_logs_new.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        textBrowser_te_logs_new.customContextMenuRequested[QtCore.QPoint].connect(self.log_right_click_menu)
        # tab创建后自动打开
        self.ui.tabWidget_te_log.setCurrentWidget(tab)
        self.opened_tab_obj_name.append(self.get_current_db_config_item())
        self.opened_text_browser_obj_name.append('text_browser_%s' % self.get_current_db_config_item())

    def print_to_new_text_browser(self, current_env, text):
        if self.ui.tabWidget_te_log.findChild(QTextBrowser,
                                              'text_browser_%s' % current_env):
            self.ui.tabWidget_te_log.findChild(QTextBrowser,
                                               'text_browser_%s' % current_env).append(text)

    def close_tab(self, index):
        self.opened_tab_obj_name.remove(self.ui.tabWidget_te_log.widget(index).objectName())
        self.opened_text_browser_obj_name.remove(
            'text_browser_%s' % self.ui.tabWidget_te_log.widget(index).objectName())
        if self.ui.tabWidget_te_log.widget(index).objectName() == 'update':
            self.log_monitor_thread.is_stop = True
            self.log_update_print_thread.is_stop = True
        elif self.ui.tabWidget_te_log.widget(index).objectName() == self.get_current_db_config_item():
            if self.thread_tab_mapping.get(self.get_current_db_config_item()) == 'biz_1':
                self.log_biz_1_monitor_thread.is_stop = True
                self.log_biz_1_print_thread.is_stop = True
                self.thread_tab_mapping.pop(self.get_current_db_config_item())
            elif self.thread_tab_mapping.get(self.get_current_db_config_item()) == 'biz_2':
                self.log_biz_2_monitor_thread.is_stop = True
                self.log_biz_2_print_thread.is_stop = True
                self.thread_tab_mapping.pop(self.get_current_db_config_item())
            elif self.thread_tab_mapping.get(self.get_current_db_config_item()) == 'biz_3':
                self.log_biz_3_monitor_thread.is_stop = True
                self.log_biz_3_print_thread.is_stop = True
                self.thread_tab_mapping.pop(self.get_current_db_config_item())

        # 使用关闭按钮传入的index，定位到要删除的tab，先使用sip删除文本框子元素，再使用sip对tab进行删除
        sip.delete(self.ui.tabWidget_te_log.findChild(QTextBrowser,
                                                      'text_browser_%s' %
                                                      self.ui.tabWidget_te_log.widget(index).objectName()))
        sip.delete(self.ui.tabWidget_te_log.findChild(QtWidgets.QWidget,
                                                      self.ui.tabWidget_te_log.widget(index).objectName()))

    def close_update_tab_auto(self):
        try:
            self.opened_tab_obj_name.remove('update')
            self.opened_text_browser_obj_name.remove('text_browser_update')
            # 使用关闭按钮传入的index，定位到要删除的tab，先使用sip删除文本框子元素，再使用sip对tab进行删除
            self.log_monitor_thread.is_stop = True
            self.log_update_print_thread.is_stop = True
            sip.delete(self.ui.tabWidget_te_log.findChild(QTextBrowser, 'text_browser_update'))
            sip.delete(self.ui.tabWidget_te_log.findChild(QtWidgets.QWidget, 'update'))
        except ValueError:
            pass

    def close_biz_tab_auto(self):
        try:
            self.opened_tab_obj_name.remove(self.get_current_db_config_item())
            self.opened_text_browser_obj_name.remove('text_browser_%s' % self.get_current_db_config_item())
            # 使用关闭按钮传入的index，定位到要删除的tab，先使用sip删除文本框子元素，再使用sip对tab进行删除
            sip.delete(self.ui.tabWidget_te_log.findChild(QTextBrowser,
                                                          'text_browser_%s' % self.get_current_db_config_item()))
            sip.delete(self.ui.tabWidget_te_log.findChild(QtWidgets.QWidget, self.get_current_db_config_item()))
        except ValueError:
            pass

    def update_log_monitor(self):
        if self.log_monitor_main_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，正在重置...')
            self.print_to_te_text_browser('如需进行日志监控，请重新启动Tomcat！')
            self.reset_update_log_monitor()
        else:
            self.log_monitor_thread.path = '%s/tomcat' % self.get_te_update_path()
            self.log_monitor_thread.port = self.get_update_port()
            self.log_monitor_thread.tab_type = 'update'
            self.thread_tab_mapping['update'] = 'update'
            self.log_monitor_main_thread.start()
            self._start_log_monitor_thread.emit()

    def biz_log_monitor(self):
        if not self.log_biz_1_print_main_thread.isRunning():
            self.log_biz_1_monitor_thread.path = self.get_te_tomcat_path()
            self.log_biz_1_monitor_thread.port = self.get_biz_port()
            self.log_biz_1_monitor_thread.url = '/t2'
            self.log_biz_1_monitor_thread.tab_type = 'biz_1'
            self.thread_tab_mapping[self.get_current_db_config_item()] = 'biz_1'
            self.log_biz_1_monitor_main_thread.start()
            self._start_biz_1_monitor_thread.emit()
        elif not self.log_biz_2_print_main_thread.isRunning():
            self.log_biz_2_monitor_thread.path = self.get_te_tomcat_path()
            self.log_biz_2_monitor_thread.port = self.get_biz_port()
            self.log_biz_2_monitor_thread.url = '/t2'
            self.log_biz_2_monitor_thread.tab_type = 'biz_2'
            self.thread_tab_mapping[self.get_current_db_config_item()] = 'biz_2'
            self.log_biz_2_monitor_main_thread.start()
            self._start_biz_2_monitor_thread.emit()
        elif not self.log_biz_3_print_main_thread.isRunning():
            self.log_biz_3_monitor_thread.path = self.get_te_tomcat_path()
            self.log_biz_3_monitor_thread.port = self.get_biz_port()
            self.log_biz_3_monitor_thread.url = '/t2'
            self.log_biz_3_monitor_thread.tab_type = 'biz_3'
            self.thread_tab_mapping[self.get_current_db_config_item()] = 'biz_3'
            self.log_biz_3_monitor_main_thread.start()
            self._start_biz_3_monitor_thread.emit()
        else:
            QMessageBox.warning(self, '提示信息', '最多支持同时启动三个业务系统Tomcat，请关闭后重试！')

    # def log_printer(self):
    #     if self.log_db_print_main_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
    #         self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
    #         return
    #     self.log_db_print_thread.current_env = self.get_current_db_config_item()
    #     self.log_db_print_main_thread.start()
    #     self._start_db_log_print_thread.emit()

    def update_log_printer(self, log_file):
        if self.log_update_print_main_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.log_update_print_thread.current_env = 'update'
        self.log_update_print_thread.log_file = log_file
        self.log_update_print_main_thread.start()
        self._start_update_log_print_thread.emit()

    def biz_1_log_printer(self, log_file):
        if self.log_biz_1_print_main_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.log_biz_1_print_thread.current_env = self.get_current_db_config_item()
        self.log_biz_1_print_thread.log_file = log_file
        self.log_biz_1_print_thread.tomcat_path = self.get_te_tomcat_path()
        self.log_biz_1_print_main_thread.start()
        self._start_biz_1_log_print_thread.emit()

    def biz_2_log_printer(self, log_file):
        if self.log_biz_2_print_main_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.log_biz_2_print_thread.current_env = self.get_current_db_config_item()
        self.log_biz_2_print_thread.log_file = log_file
        self.log_biz_2_print_thread.tomcat_path = self.get_te_tomcat_path()
        self.log_biz_2_print_main_thread.start()
        self._start_biz_2_log_print_thread.emit()

    def biz_3_log_printer(self, log_file):
        if self.log_biz_3_print_main_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.log_biz_3_print_thread.current_env = self.get_current_db_config_item()
        self.log_biz_3_print_thread.log_file = log_file
        self.log_biz_3_print_thread.tomcat_path = self.get_te_tomcat_path()
        self.log_biz_3_print_main_thread.start()
        self._start_biz_3_log_print_thread.emit()

    def update_log_printer_starter(self, log_file):
        self.new_update_log_tab()
        self.update_log_printer(log_file)

    def biz_1_log_printer_starter(self, log_file):
        self.new_log_tab()
        self.biz_1_log_printer(log_file)

    def biz_2_log_printer_starter(self, log_file):
        self.new_log_tab()
        self.biz_2_log_printer(log_file)

    def biz_3_log_printer_starter(self, log_file):
        self.new_log_tab()
        self.biz_3_log_printer(log_file)

    def port_check(self, check_biz: bool):
        if len(self.thread_tab_mapping) == 4:
            QMessageBox.warning(self, '提示信息', '最多支持同时启动四个Tomcat，请关闭后重试！')
            return
        if self.port_check_main_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        if check_biz:
            self.port_check_thread.biz_port = self.get_biz_port()
        else:
            self.port_check_thread.update_port = self.get_update_port()
        self.port_check_main_thread.start()
        self._start_port_check_thread.emit()

    def save_tested_biz_port(self, port_test_result):
        self.is_te_biz_port_tested = port_test_result
        self.tested_biz_port = self.get_biz_port()

    def save_tested_update_port(self, port_test_result):
        self.is_te_update_port_tested = port_test_result
        self.tested_update_port = self.get_update_port()

    def set_db_test_flag(self, result):
        self.is_te_db_tested = result

    def set_db_tested_config(self, config):
        self.tested_te_db_config.clear()
        self.tested_te_db_config = config

    def set_be_db_test_flag(self, result):
        self.is_be_db_tested = result

    def set_be_db_tested_config(self, config):
        self.tested_be_db_config.clear()
        self.tested_be_db_config = config

    def show_save_db_config(self):
        self.child_save_db_config.show()
        self.child_save_db_config.set_default_text('%s - %s' % (self.get_te_db_type(), self.get_te_db_name()))

    # def init(self):
    #     self.print_to_te_text_browser()

    def closeEvent(self, event) -> None:
        # thread_running_list = [self.init_thread.isRunning(),
        #                        self.server_thread.isRunning(),
        #                        self.oracle_server_thread.isRunning(),
        #                        self.check_connection_thread.isRunning(),
        #                        self.check_be_connection_thread.isRunning(),
        #                        self.get_connection_thread.isRunning(),
        #                        self.get_init_connection_thread.isRunning(),
        #                        self.get_run_sql_connection_thread.isRunning(),
        #                        self.run_sql_thread.isRunning(),
        #                        self.structure_thread.isRunning(),
        #                        self.update_structure_main_thread.isRunning(),
        #                        self.patch_thread.isRunning(),
        #                        self.update_patch_main_thread.isRunning(),
        #                        self.start_t2_main_thread.isRunning(),
        #                        self.port_check_main_thread.isRunning(),
        #                        self.log_monitor_main_thread.isRunning(),
        #                        self.log_biz_1_monitor_main_thread.isRunning(),
        #                        self.log_biz_2_monitor_main_thread.isRunning(),
        #                        self.log_biz_3_monitor_main_thread.isRunning(),
        #                        self.log_db_print_main_thread.isRunning(),
        #                        self.log_update_print_main_thread.isRunning(),
        #                        self.log_biz_1_print_main_thread.isRunning(),
        #                        self.log_biz_2_print_main_thread.isRunning(),
        #                        self.log_biz_3_print_main_thread.isRunning(),
        #                        self.bank_update_main_thread.isRunning(),
        #                        self.unzip_war_package_main_thread.isRunning()]
        # if any(thread_running_list):
        #     print(thread_running_list)

        if len(self.started_tomcat_port) != 0:
            if QMessageBox.question(self,
                                    '提示信息',
                                    '退出程序会同时终止所有通过程序启动的Tomcat，是否确认退出？') == QMessageBox.StandardButton.Yes:
                for _ in self.started_tomcat_port:
                    kill_process(_)
                self.save_config()
                self.emit_stop_for_all_monitor()
                event.accept()
                remove_temp_tree()
            else:
                event.ignore()
        else:
            self.save_config()
            event.accept()
            remove_temp_tree()

    def emit_stop_for_all_monitor(self):
        self.log_db_print_thread.is_stop = True
        self.log_update_print_thread.is_stop = True
        self.log_biz_1_print_thread.is_stop = True
        self.log_biz_2_print_thread.is_stop = True
        self.log_biz_3_print_thread.is_stop = True
        self.log_monitor_thread.is_stop = True
        self.log_biz_1_monitor_thread.is_stop = True
        self.log_biz_2_monitor_thread.is_stop = True
        self.log_biz_3_monitor_thread.is_stop = True
        self.log_biz_1_print_main_thread.quit()
        self.log_biz_2_print_main_thread.quit()
        self.log_biz_3_print_main_thread.quit()
        self.log_update_print_main_thread.quit()
        self.log_monitor_main_thread.quit()
        self.log_biz_1_monitor_main_thread.quit()
        self.log_biz_2_monitor_main_thread.quit()
        self.log_biz_3_monitor_main_thread.quit()

    def save_config(self):
        save_config(t2_db_conf_name=self.get_current_db_config_item(),
                    t2_db_type=self.get_te_db_type(),
                    t2_db_ip=self.get_te_db_ip(),
                    t2_db_name=self.get_te_db_name(),
                    t2_db_user=self.get_te_db_user(),
                    t2_db_password=self.get_te_db_password(),
                    t2_program_path=self.get_te_program_path(),
                    t2_tomcat_path=self.get_te_tomcat_path(),
                    t2_update_path=self.get_te_update_path(),
                    t2_biz_port=self.get_biz_port(),
                    t2_update_port=self.get_update_port(),
                    bank_db_type=self.get_be_db_type(),
                    bank_db_ip=self.get_be_db_ip(),
                    bank_db_name=self.get_be_db_name(),
                    bank_db_user=self.get_be_db_user(),
                    bank_db_password=self.get_be_db_password(),
                    bank_redis_path=self.get_be_redis_path(),
                    bank_server_path=self.get_be_server_path(),
                    bank_client_path=self.get_be_client_path(),
                    bank_redis_port=self.get_be_redis_port(),
                    bank_server_port=self.get_be_server_port(),
                    bank_client_port=self.get_be_client_port(),
                    bank_log_path=self.get_be_logs_path(),
                    bank_war_path=self.get_be_war_path(),
                    bank_type=self.get_be_bank_type())

    def set_config(self):
        try:
            previous_data = read_yaml('%s\\data\\saved_ui_conf.yml' % get_current_path())
            if previous_data is not None:
                t2_conf = previous_data['data']['t2']
                self.set_current_db_config_item(t2_conf['db']['t2_db_conf_name'])
                self.set_te_db_type(t2_conf['db']['t2_db_type'])
                self.set_te_db_ip(t2_conf['db']['t2_db_ip'])
                self.set_te_db_name(t2_conf['db']['t2_db_name'])
                self.set_te_db_user(t2_conf['db']['t2_db_user'])
                self.set_te_db_password(t2_conf['db']['t2_db_password'])
                self.set_te_program_path(t2_conf['path']['t2_program_path'])
                self.set_te_tomcat_path(t2_conf['path']['t2_tomcat_path'])
                self.set_te_update_path(t2_conf['path']['t2_update_path'])
                self.set_biz_port(t2_conf['path']['t2_biz_port'])
                self.set_update_port(t2_conf['path']['t2_update_port'])
                bank_conf = previous_data['data']['bank']
                self.set_be_db_type(bank_conf['db']['bank_db_type'])
                self.set_be_db_ip(bank_conf['db']['bank_db_ip'])
                self.set_be_db_name(bank_conf['db']['bank_db_name'])
                self.set_be_db_user(bank_conf['db']['bank_db_user'])
                self.set_be_db_password(bank_conf['db']['bank_db_password'])
                self.set_be_redis_path(bank_conf['path']['bank_redis_path'])
                self.set_be_redis_port(bank_conf['path']['bank_redis_port'])
                self.set_be_server_path(bank_conf['path']['bank_server_path'])
                self.set_be_server_port(bank_conf['path']['bank_server_port'])
                self.set_be_client_path(bank_conf['path']['bank_client_path'])
                self.set_be_client_port(bank_conf['path']['bank_client_port'])
                self.set_be_logs_path(bank_conf['path']['bank_log_path'])
                self.set_be_war_path(bank_conf['path']['bank_war_path'])
        except KeyError:
            return

    def log_right_click_menu(self):
        popMenu = QMenu()
        clear_action = QAction(u'清空', self)
        clear_action.triggered.connect(self.clear_te_logs)
        popMenu.addAction(clear_action)
        popMenu.exec(QCursor.pos())

    def be_log_right_click_menu(self):
        popMenu = QMenu()
        clear_action = QAction(u'清空', self)
        clear_action.triggered.connect(self.clear_be_logs)
        popMenu.addAction(clear_action)
        popMenu.exec(QCursor.pos())

    def save_config_right_click_menu(self):
        popMenu = QMenu()
        delete_action = QAction(u'删除配置', self)
        delete_action.triggered.connect(self.delete_db_config)
        popMenu.addAction(delete_action)
        popMenu.exec(QCursor.pos())

    def save_be_config_right_click_menu(self):
        popMenu = QMenu()
        delete_action = QAction(u'删除配置', self)
        delete_action.triggered.connect(self.delete_bank_config)
        popMenu.addAction(delete_action)
        popMenu.exec(QCursor.pos())

    def start_update_right_click_menu(self):
        popMenu = QMenu()
        delete_action = QAction(u'关闭升级工具', self)
        delete_action.triggered.connect(self.close_update_tab_auto)
        delete_action.triggered.connect(lambda: self.shutdown_te_process(self.get_update_port()))
        popMenu.addAction(delete_action)
        popMenu.exec(QCursor.pos())

    def start_t2_right_click_menu(self):
        popMenu = QMenu()
        delete_action = QAction(u'关闭业务系统', self)
        delete_action.triggered.connect(self.close_biz_tab_auto)
        delete_action.triggered.connect(lambda: self.shutdown_te_process(self.get_biz_port()))
        popMenu.addAction(delete_action)
        popMenu.exec(QCursor.pos())

    def start_redis_right_click_menu(self):
        popMenu = QMenu()
        delete_action = QAction(u'关闭Redis', self)
        delete_action.triggered.connect(lambda: self.shutdown_be_process(self.get_be_redis_port()))
        popMenu.addAction(delete_action)
        popMenu.exec(QCursor.pos())

    def start_client_right_click_menu(self):
        popMenu = QMenu()
        delete_action = QAction(u'关闭客户端', self)
        delete_action.triggered.connect(lambda: self.shutdown_be_process(self.get_be_client_port()))
        popMenu.addAction(delete_action)
        popMenu.exec(QCursor.pos())

    def start_server_right_click_menu(self):
        popMenu = QMenu()
        delete_action = QAction(u'关闭服务端', self)
        delete_action.triggered.connect(lambda: self.shutdown_be_process(self.get_be_server_port()))
        popMenu.addAction(delete_action)
        popMenu.exec(QCursor.pos())

    def shutdown_te_process(self, port):
        if port:
            try:
                self.print_to_te_text_browser('正在停止监控...')
                if self.thread_tab_mapping.get(self.get_current_db_config_item(), '') == 'biz_1':
                    self.log_biz_1_print_thread.is_stop = True
                    self.log_biz_1_monitor_thread.is_stop = True
                    self.log_biz_1_monitor_thread.flag = False
                    self.thread_tab_mapping.pop(self.get_current_db_config_item())
                    self.log_biz_1_print_main_thread.quit()
                    self.log_biz_1_print_main_thread.wait()
                    self.log_biz_1_monitor_main_thread.quit()
                    self.log_biz_1_monitor_main_thread.wait()
                elif self.thread_tab_mapping.get(self.get_current_db_config_item(), '') == 'biz_2':
                    self.log_biz_2_print_thread.is_stop = True
                    self.log_biz_2_monitor_thread.is_stop = True
                    self.log_biz_2_monitor_thread.flag = False
                    self.thread_tab_mapping.pop(self.get_current_db_config_item())
                    self.log_biz_2_print_main_thread.quit()
                    self.log_biz_2_print_main_thread.wait()
                    self.log_biz_2_monitor_main_thread.quit()
                    self.log_biz_2_monitor_main_thread.wait()
                elif self.thread_tab_mapping.get(self.get_current_db_config_item(), '') == 'biz_3':
                    self.log_biz_3_print_thread.is_stop = True
                    self.log_biz_3_monitor_thread.is_stop = True
                    self.log_biz_3_monitor_thread.flag = False
                    self.thread_tab_mapping.pop(self.get_current_db_config_item())
                    self.log_biz_3_print_main_thread.quit()
                    self.log_biz_3_print_main_thread.wait()
                    self.log_biz_3_monitor_main_thread.quit()
                    self.log_biz_3_monitor_main_thread.wait()
                elif self.thread_tab_mapping.get('update', '') == 'update':
                    self.log_update_print_thread.is_stop = True
                    self.log_monitor_thread.is_stop = True
                    self.log_monitor_thread.flag = False
                    self.thread_tab_mapping.pop('update')
                    self.log_update_print_main_thread.quit()
                    self.log_update_print_main_thread.wait()
                    self.log_monitor_main_thread.quit()
                    self.log_monitor_main_thread.wait()
                self.print_to_te_text_browser('正在尝试终止端口号为%s的进程...' % port)
                self.started_tomcat_port.remove(port)
                kill_result = kill_process(port)
                self.print_to_te_text_browser(kill_result)
            except ValueError:
                self.print_to_te_text_browser('端口号为%s的进程已关闭或该进程不是通过程序启动的，无法关闭！' % port)
        else:
            self.print_to_te_text_browser('端口号未输入，无法关闭！')

    def shutdown_be_process(self, port):
        if port:
            try:
                self.print_to_be_text_browser('正在尝试终止端口号为%s的进程...' % port)
                self.started_tomcat_port.remove(port)
                kill_result = kill_process(port)
                self.print_to_be_text_browser(kill_result)
            except ValueError:
                self.print_to_be_text_browser('端口号为%s的进程已关闭或该进程不是通过程序启动的，无法关闭！' % port)
        else:
            self.print_to_be_text_browser('端口号未输入，无法关闭！')

    def update_patch(self):
        self.started_tomcat_port.append(self.get_update_port())
        self.save_te_db_config(self.current_te_db_config)
        if self.is_te_db_tested:
            if self.check_te_db_config_diff(self.tested_te_db_config, self.current_te_db_config):
                if not self.get_te_update_path():
                    self.print_to_te_text_browser('请输入升级工具路径！')
                else:
                    if not self.get_update_port():
                        self.print_to_te_text_browser('请输入升级工具端口！')
                    else:
                        if not check_path(self.get_te_update_path(), 'tomcat', 'autoupdate', 'patches'):
                            self.print_to_te_text_browser('升级工具路径输入有误！')
                        else:
                            self.port_check(False)
            else:
                self.print_to_te_text_browser('检测到数据库配置信息改变，请重新执行数据库连接测试！')
        else:
            self.print_to_te_text_browser('请先执行数据库连接测试！')

    def update_patch_pre(self):
        if self.get_te_patch_path() and self.get_te_update_patch_name():
            self.print_to_te_text_browser('检测到构建包路径和构建包名称同时录入！\n请保留构建包路径或构建包名称后重新执行！')
        elif self.get_te_patch_path():
            self.update_patch_manual()
        elif self.get_te_patch_path() or self.get_te_patch_path() == '':
            self.update_patch_auto()
        else:
            self.print_to_te_text_browser('请输入正确的构建包路径或构建包名称！')

    def update_patch_manual(self):
        if is_dir(self.get_te_patch_path()):
            current_patch_path_files = get_all_filepath(self.get_te_patch_path(), 'patch')
            if current_patch_path_files and not self.get_te_update_patch_name():
                final_patch_path = []
                for _ in current_patch_path_files:
                    if check_patch_name(_.split('\\')[-1]):
                        final_patch_path.append(convert_slash(_))
                self.print_to_te_text_browser(
                    '补丁包路径下找到%s个符合条件的patch包：%s' % (len(final_patch_path), ','.join(final_patch_path)))
                if len(final_patch_path) == 1:
                    self.print_to_te_text_browser('复制补丁包到临时目录...')
                    copy_result = copy_file(final_patch_path[0], '.\\data\\temp')
                    if copy_result:
                        self.print_to_te_text_browser('文件复制完成！')
                        self.update_patch_main()
                    else:
                        self.print_to_te_text_browser('部分或全部文件复制失败，请检查后重试！')
                else:
                    self.print_to_te_text_browser('不支持多补丁包更新，请在目录下仅保留一个后重试！')
            else:
                self.print_to_te_text_browser('补丁包路径下未找到patch文件！')
        else:
            self.print_to_te_text_browser('请输入正确的补丁包路径！')

    def update_patch_auto(self):
        if self.patch_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.get_patch_thread.patch_name = self.get_te_update_patch_name()
        self.patch_thread.start()
        self._start_get_patch_thread.emit()

    def update_patch_main(self):
        if self.update_patch_main_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.update_patch_thread.update_platform_path = self.get_te_update_path()
        self.update_patch_thread.db_type = self.get_te_db_type()
        self.update_patch_thread.ip = self.get_te_db_ip().split(':')[0]
        self.update_patch_thread.port = self.get_te_db_ip().split(':')[-1]
        self.update_patch_thread.user = self.get_te_db_user()
        self.update_patch_thread.password = self.get_te_db_password()
        self.update_patch_thread.db = self.get_te_db_name()
        self.update_patch_thread.patch_name = self.get_te_update_patch_name()
        self.update_patch_thread.is_port_tested = self.is_te_update_port_tested
        self.update_patch_thread.tested_port = self.tested_update_port
        self.update_patch_thread.update_platform_port = self.get_update_port()
        self.update_patch_main_thread.start()
        self._start_update_patch_thread.emit()

    def update_structure(self):
        self.save_te_db_config(self.current_te_db_config)
        if self.is_te_db_tested:
            if self.check_te_db_config_diff(self.tested_te_db_config, self.current_te_db_config):
                if not self.get_te_program_path():
                    self.print_to_te_text_browser('请输入程序包路径！')
                else:
                    if not check_path(self.get_te_program_path(), 'WEB-INF', 'static'):
                        self.print_to_te_text_browser('程序包路径输入有误！')
                    else:
                        if self.get_te_structure_path() and self.get_te_structure_name():
                            self.print_to_te_text_browser('检测到构建包路径和构建包名称同时录入！\n请保留构建包路径或构建包名称后重新执行！')
                        elif self.get_te_structure_path():
                            self.update_structure_manual()
                        elif self.get_te_structure_name():
                            self.update_structure_auto()
                        else:
                            self.print_to_te_text_browser('请输入正确的构建包路径或构建包名称！')
            else:
                self.print_to_te_text_browser('检测到数据库配置信息改变，请重新执行数据库连接测试！')
        else:
            self.print_to_te_text_browser('请先执行数据库连接测试！')

    def update_structure_manual(self):
        if is_dir(self.get_te_structure_path()):
            current_structure_path_zip_files = get_all_filepath(self.get_te_structure_path(), '.zip')

            if current_structure_path_zip_files and not self.get_te_structure_name():
                final_zip_path = []
                copy_result_list = []
                for _ in current_structure_path_zip_files:
                    if check_structure_name(_.split('\\')[-1][:-4]):
                        final_zip_path.append(convert_slash(_))

                self.print_to_te_text_browser('构建包路径下找到%s个符合条件的zip包：' % len(final_zip_path))
                for _ in final_zip_path:
                    self.print_to_te_text_browser('复制%s到临时目录...' % _.split('/')[-1])
                    copy_result = copy_file(_, '.\\data\\temp')
                    copy_result_list.append(copy_result)
                if copy_result_list and all(copy_result_list):
                    self.print_to_te_text_browser('文件复制完成！')
                    self.update_structure_main()
                else:
                    self.print_to_te_text_browser('部分或全部文件复制失败，请检查后重试！')
            else:
                self.print_to_te_text_browser('构建包路径下未找到zip压缩包！')
        else:
            self.print_to_te_text_browser('请输入正确的构建包路径！')

    def update_structure_auto(self):
        self.print_to_te_text_browser('构建包名称已录入，正在检测构建包名称...')
        check_result = check_structure_name(self.get_te_structure_name())

        if any([isinstance(check_result, list) and all(check_result),
                isinstance(check_result, bool) and check_result]):
            self.print_to_te_text_browser('检测通过，开始执行构建包拉取...')

            if self.structure_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
                self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
                return
            self.get_structure_thread.structure_name = self.get_te_structure_name()
            self.structure_thread.start()
            self._start_get_structure_thread.emit()

        elif isinstance(check_result, list) and any(check_result):
            false_structure_index = []
            false_structure_name = []

            for _ in check_result:
                if not _:
                    false_structure_index.append(check_result.index(_))

            for _ in false_structure_index:
                false_structure_name.append(self.get_te_structure_name().split(',')[_])

            self.print_to_te_text_browser(
                '检测不通过，共%s个构建包名称输入有误：%s\n请重新输入！' % (
                    len(false_structure_index), ','.join(false_structure_name)))
        else:
            self.print_to_te_text_browser('构建包名称输入有误：%s\n请重新输入！' % self.get_te_structure_name())

    def update_structure_main(self):
        if self.update_structure_main_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.update_structure_thread.program_path = self.get_te_program_path()
        # self.update_structure_thread.structure_path = self.get_te_structure_path()
        self.update_structure_thread.is_db_tested = self.is_te_db_tested
        self.update_structure_thread.db_type = self.get_te_db_type()
        self.update_structure_thread.ip = self.get_te_db_ip().split(':')[0]
        self.update_structure_thread.port = self.get_te_db_ip().split(':')[-1]
        self.update_structure_thread.user = self.get_te_db_user()
        self.update_structure_thread.password = self.get_te_db_password()
        self.update_structure_thread.db = self.get_te_db_name()
        self.update_structure_main_thread.start()
        self._start_update_structure_thread.emit()

    def start_t2(self):
        if self.start_t2_main_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.start_t2_thread.tomcat_path = self.get_te_tomcat_path()
        self.start_t2_main_thread.start()
        self._start_t2_thread.emit()

    # def get_te_sys_jdk_path(self):
    #     if get_sys_jdk_path():
    #         self.ui.lineEdit_te_jdk_path.setText(convert_slash(get_sys_jdk_path()))
    #     else:
    #         QMessageBox.warning(self, '提示信息', '系统环境变量中未定义JAVA_HOME！')

    def check_te_db_config_diff(self, tested_te_db_config, current_te_db_config):
        if tested_te_db_config == current_te_db_config:
            return True
        else:
            self.is_te_db_tested = False

    def check_te_path_config_diff(self, tested_te_path_config, current_te_path_config):
        if tested_te_path_config == current_te_path_config:
            return True
        else:
            self.is_te_env_configured = False

    def check_be_db_config_diff(self, tested_be_db_config, current_be_db_config):
        if tested_be_db_config == current_be_db_config:
            return True
        else:
            self.is_be_db_tested = False

    def check_be_path_config_diff(self, tested_be_path_config, current_be_path_config):
        if tested_be_path_config == current_be_path_config:
            return True
        else:
            self.is_be_env_configured = False

    def save_te_db_config(self, db_config_list):
        db_config_list.clear()
        db_config_list.append(self.get_te_db_type())
        db_config_list.append(self.get_te_db_ip())
        db_config_list.append(self.get_te_db_user())
        db_config_list.append(self.get_te_db_password())
        db_config_list.append(self.get_te_db_name())
        return db_config_list

    def save_be_db_config(self, db_config_list):
        db_config_list.clear()
        db_config_list.append(self.get_be_db_type())
        db_config_list.append(self.get_be_db_ip())
        db_config_list.append(self.get_be_db_user())
        db_config_list.append(self.get_be_db_password())
        db_config_list.append(self.get_be_db_name())
        return db_config_list

    def load_saved_db_config(self):
        try:
            self.ui.comboBox_te_db_config_name.clear()
            saved_db_config_names = read_yaml(r'.\data\saved_db_conf.yml')['data']['saved_db_config']
            self.ui.comboBox_te_db_config_name.addItems([*saved_db_config_names])
        except TypeError:
            return

    def switch_current_db_config(self):
        saved_db_config_dict = read_yaml(r'.\data\saved_db_conf.yml')
        if saved_db_config_dict:
            try:
                current_db_config_details = \
                    saved_db_config_dict['data']['saved_db_config'][self.get_current_db_config_item()][0]
                self.set_te_db_type(current_db_config_details.get('db_type', ''))
                self.set_te_db_ip(current_db_config_details['db_ip'])
                self.set_te_db_name(current_db_config_details['db_name'])
                self.set_te_db_user(current_db_config_details['db_user'])
                self.set_te_db_password(current_db_config_details['db_password'])
                self.set_te_program_path(current_db_config_details['program_path'])
                self.set_te_tomcat_path(current_db_config_details['tomcat_path'])
                self.set_biz_port(current_db_config_details['biz_port'])
                self.set_te_update_path(current_db_config_details['update_path'])
                self.set_update_port(current_db_config_details['update_port'])
            except (TypeError, KeyError):
                return

    def delete_db_config(self):
        if len(self.get_current_db_config_items()):
            saved_db_config_dict = read_yaml(r'.\data\saved_db_conf.yml')
            if saved_db_config_dict['data']['saved_db_config']:
                saved_db_config_dict['data']['saved_db_config'].pop(self.get_current_db_config_item())
                clear_yaml(r'.\data\saved_db_conf.yml')
                write_yaml(r'.\data\saved_db_conf.yml', saved_db_config_dict)
                self.print_to_te_text_browser('当前配置已删除！')
                self.load_saved_db_config()
                self.switch_current_db_config()
        else:
            self.print_to_te_text_browser('无已保存的配置!')

    def check_te_db_config(self):
        if not self.get_te_db_ip():
            self.print_to_te_text_browser('请输入主机/端口！')
        elif not check_url(self.get_te_db_ip()):
            self.print_to_te_text_browser('主机/端口输入格式不正确，请重新输入！\n例：127.0.0.1:3306')
        elif not self.get_te_db_name():
            self.print_to_te_text_browser('请输入数据库名称！')
        elif not self.get_te_db_user():
            self.print_to_te_text_browser('请输入用户名！')
        elif not self.get_te_db_password():
            self.print_to_te_text_browser('请输入密码！')
        else:
            self.show_save_db_config()

    def get_current_db_config_item(self):
        return self.ui.comboBox_te_db_config_name.currentText()

    def set_current_db_config_item(self, text):
        self.ui.comboBox_te_db_config_name.setCurrentText(text)

    def get_current_db_config_items(self):
        current_items = []
        for i in range(self.ui.comboBox_te_db_config_name.count()):
            current_items.append(self.ui.comboBox_te_db_config_name.itemText(i))
        return current_items

    def save_te_db_config_to_yml(self):
        save_db_config(config_name=self.child_save_db_config.get_current_text(),
                       db_type=self.get_te_db_type(),
                       db_ip=self.get_te_db_ip(),
                       db_name=self.get_te_db_name(),
                       db_user=self.get_te_db_user(),
                       db_password=self.get_te_db_password(),
                       program_path=self.get_te_program_path(),
                       tomcat_path=self.get_te_tomcat_path(),
                       biz_port=self.get_biz_port(),
                       update_path=self.get_te_update_path(),
                       update_port=self.get_update_port())
        if self.child_save_db_config.get_current_text() not in self.get_current_db_config_items():
            self.ui.comboBox_te_db_config_name.addItem(self.child_save_db_config.get_current_text())
        self.ui.comboBox_te_db_config_name.setCurrentText(self.child_save_db_config.get_current_text())
        self.child_save_db_config.close()
        self.print_to_te_text_browser('当前配置保存成功！')

    def save_te_path_config(self, path_config_list):
        path_config_list.clear()
        path_config_list.append(self.get_te_program_path())
        path_config_list.append(self.get_te_tomcat_path())
        return path_config_list

    def save_be_path_config(self, path_config_list):
        path_config_list.clear()
        path_config_list.append(self.get_be_client_path())
        path_config_list.append(self.get_be_server_path())
        path_config_list.append(self.get_be_war_path())
        return path_config_list

    def restore_start_t2_button(self):
        self.ui.pushButton_te_start_t2.setEnabled(True)
        self.ui.pushButton_te_start_update.setEnabled(True)

    def lock_start_t2_button(self):
        self.ui.pushButton_te_start_t2.setEnabled(False)
        self.ui.pushButton_te_start_update.setEnabled(False)

    def te_path_config(self):
        self.started_tomcat_port.append(self.get_biz_port())
        self.save_te_db_config(self.current_te_db_config)
        if self.is_te_db_tested:
            if self.check_te_db_config_diff(self.tested_te_db_config, self.current_te_db_config):
                if not self.get_te_program_path():
                    self.print_to_te_text_browser('请输入程序包路径！')
                elif not self.get_te_tomcat_path():
                    self.print_to_te_text_browser('请输入Tomcat路径！')
                else:
                    if not check_path(self.get_te_program_path(), 'WEB-INF', 'static'):
                        self.print_to_te_text_browser('程序包路径输入有误！')
                    elif not check_path(self.get_te_tomcat_path(), 'bin', 'conf'):
                        self.print_to_te_text_browser('tomcat路径输入有误！')
                    elif not self.get_biz_port():
                        self.print_to_te_text_browser('请输入业务系统端口号！')
                    else:
                        self.port_check(True)
            else:
                self.print_to_te_text_browser('检测到数据库配置信息改变，请重新执行数据库连接测试！')
        else:
            self.print_to_te_text_browser('请先执行数据库连接测试！')

    def check_te_db_connection(self):
        if not self.get_te_db_ip():
            self.print_to_te_text_browser('请输入主机/端口！')
        elif not check_url(self.get_te_db_ip()):
            self.print_to_te_text_browser('主机/端口输入格式不正确，请重新输入！\n例：127.0.0.1:3306')
        elif not self.get_te_db_name():
            self.print_to_te_text_browser('请输入数据库名称！')
        elif not self.get_te_db_user():
            self.print_to_te_text_browser('请输入用户名！')
        elif not self.get_te_db_password():
            self.print_to_te_text_browser('请输入密码！')
        else:
            self.check_db_connection()

    def pre_run_init_sql(self):
        is_run = QMessageBox.question(self, '提示信息', '检测到MySql服务正在运行,是否执行数据库初始化？')
        if is_run == QMessageBox.StandardButton.Yes:
            self.print_to_te_text_browser('检查当前数据库连接情况...')
            if self.get_connection_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
                self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
                return
            self.get_db_connection_thread.db_type = self.get_te_db_type()
            self.get_db_connection_thread.ip = self.get_te_db_ip().split(':')[0]
            self.get_db_connection_thread.port = self.get_te_db_ip().split(':')[-1]
            self.get_db_connection_thread.user = self.get_te_db_user()
            self.get_db_connection_thread.password = self.get_te_db_password()
            self.get_db_connection_thread.db = self.get_te_db_name()
            self.get_connection_thread.start()
            self._start_get_db_connection_thread.emit()
        else:
            self.print_to_te_text_browser('用户取消执行初始化MySql')
            self.ui.pushButton_te_install_mysql.setEnabled(True)

    def is_inited(self, connect):
        self.print_to_te_text_browser('检查当前数据库是否执行过初始化...')
        is_executed, msg = query_sql(connect.cursor(), 'select bs_ver from version_current')
        if is_executed:
            self.print_to_te_text_browser('当前数据库已执行过初始化，请进行环境配置！\n版本信息：%s' % msg)
            self.ui.pushButton_te_install_mysql.setEnabled(True)
        else:
            self.print_to_te_text_browser('当前数据库未执行过初始化！')
            self.run_init_sql()

    def run_init_sql(self):
        if self.run_sql_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        # self.run_init_sql_thread.connect = connect
        self.run_init_sql_thread.db_type = self.get_te_db_type()
        self.run_init_sql_thread.ip = self.get_te_db_ip().split(':')[0]
        self.run_init_sql_thread.port = self.get_te_db_ip().split(':')[-1]
        self.run_init_sql_thread.user = self.get_te_db_user()
        self.run_init_sql_thread.password = self.get_te_db_password()
        self.run_init_sql_thread.db = self.get_te_db_name()
        self.run_sql_thread.start()
        self._start_run_init_sql_thread.emit()

    def database_init(self):
        self.ui.pushButton_te_install_mysql.setEnabled(False)
        if self.get_te_db_ip().split(':')[0] == '127.0.0.1':
            if self.get_te_db_type() == 'MySQL':
                self.print_to_te_text_browser('正在检查MySql服务是否已启动...')
                is_running, msg = check_service('mysql')
                # is_running = False
                # msg = 'test'
                if is_running:
                    self.print_to_te_text_browser(msg)
                    # self.pre_run_init_sql()
                    self.pre_check_connect()
                elif not is_running and 'STOPPED' in msg:
                    self.print_to_te_text_browser(msg)
                    self.start_mysql_server()
                else:
                    # self.set_te_db_ip('127.0.0.1:3306')
                    # self.install_mysql()
                    self.print_to_te_text_browser('未检测到%s服务，请自行安装后重试！' % self.get_te_db_type())
            elif self.get_te_db_type() == 'Oracle':
                self.print_to_te_text_browser('正在检查Oracle服务是否已启动...')
                is_running, msg = check_service('oracleservice%s' % self.get_te_db_name())
                if is_running:
                    self.print_to_te_text_browser(msg)
                    self.pre_check_connect()
                elif not is_running and 'STOPPED' in msg:
                    self.print_to_te_text_browser(msg)
                    self.start_oracle_server()
                else:
                    self.print_to_te_text_browser('未检测到%s服务，请自行安装后重试！' % self.get_te_db_type())
        else:
            self.pre_check_connect()

    def pre_check_connect(self):
        if not self.get_te_db_ip():
            self.print_to_te_text_browser('请输入主机/端口！')
        elif not check_url(self.get_te_db_ip()):
            self.print_to_te_text_browser('主机/端口输入格式不正确，请重新输入！\n例：127.0.0.1:3306')
        elif not self.get_te_db_name():
            self.print_to_te_text_browser('请输入数据库名称！')
        elif not self.get_te_db_user():
            self.print_to_te_text_browser('请输入用户名！')
        elif not self.get_te_db_password():
            self.print_to_te_text_browser('请输入密码！')
        else:
            self.check_db_connection(is_init=True)

    def show_root_login(self, test_result):
        if test_result:
            is_run = QMessageBox.question(self, '提示信息', '当前数据库信息连接成功，是否立即执行初始化？')
            if is_run == QMessageBox.StandardButton.Yes:
                self.execute_init_sql()
        else:
            self.child_root_login.ip = self.get_te_db_ip().split(':')[0]
            self.child_root_login.port = self.get_te_db_ip().split(':')[-1]
            self.child_root_login.db_type = self.get_te_db_type()
            if self.get_te_db_type() == 'Oracle':
                self.child_root_login.db = self.get_te_db_name()
            self.child_root_login.show()
            self.child_root_login.set_default_user(self.get_te_db_type())

    def get_init_db_connection(self):
        if self.get_init_connection_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.get_init_db_connection_thread.db_type = self.get_te_db_type()
        self.get_init_db_connection_thread.ip = self.get_te_db_ip().split(':')[0]
        self.get_init_db_connection_thread.port = self.get_te_db_ip().split(':')[-1]
        self.get_init_db_connection_thread.user = self.get_te_db_user()
        self.get_init_db_connection_thread.password = self.get_te_db_password()
        self.get_init_db_connection_thread.db = None
        self.print_to_te_text_browser('正在尝试使用初始用户和密码进行数据库连接...')
        self.get_init_connection_thread.start()
        self._start_get_init_db_connection_thread.emit()

    def create_user_and_database(self, connect):
        self.child_root_login.close()
        if self.get_te_db_type() == 'MySQL':
            is_run = QMessageBox.question(self, '提示信息', '是否确认根据当前页面输入的信息创建%s数据库和用户？' % self.get_te_db_type())
            if is_run == QMessageBox.StandardButton.Yes:
                # self.print_to_te_text_browser('正在修改root用户初始密码...')
                # change_init_password_statement = "SET PASSWORD FOR root@localhost = '123456'"
                # is_user_created, msg = run_sql(connect, change_init_password_statement)
                # self.print_to_te_text_browser(msg)
                self.print_to_te_text_browser('正在创建用户...')

                # user = 't_user_%s_%s' % (get_current_date(), random_str())
                user = self.get_te_db_user()
                password = self.get_te_db_password()
                create_user_statement = "create user '%s'@'%%' identified by '%s';" % (user, password)
                grant_privileges_statement = "grant all privileges on *.* to '%s'@'%%';" % user
                is_user_created, create_user_msg = mysql_run_sql(connect, create_user_statement)
                is_granted_privileges, grant_msg = mysql_run_sql(connect, grant_privileges_statement)

                if is_user_created and is_granted_privileges:
                    self.print_to_te_text_browser('%s\n用户：%s\n密码：%s' % (create_user_msg, user, password))
                    # self.ui.lineEdit_te_db_user.setText(user)
                    # self.ui.lineEdit_te_db_password.setText(user)

                    self.print_to_te_text_browser('正在创建数据库...')
                    # database_name = 't_database_%s_%s' % (get_current_date(), random_str())
                    database_name = self.get_te_db_name()
                    create_database_statement = "create database %s character set utf8;" % database_name
                    is_database_created, create_database_msg = mysql_run_sql(connect, create_database_statement)

                    if is_database_created:
                        self.print_to_te_text_browser('%s\n数据库：%s' % (create_database_msg, database_name))
                        # self.ui.lineEdit_te_db_name.setText(database_name)

                        is_run = QMessageBox.question(self, '提示信息', '用户、数据库创建完成，是否立即执行数据库初始化？')
                        if is_run == QMessageBox.StandardButton.Yes:
                            self.execute_init_sql()
                        else:
                            self.print_to_te_text_browser('用户取消初始化操作！')
                    else:
                        self.print_to_te_text_browser('创建数据库失败！\n%s' % create_database_msg)
                else:
                    self.print_to_te_text_browser('创建用户失败！\n%s' % create_user_msg)
            else:
                self.print_to_te_text_browser('用户取消初始化操作！')
        elif self.get_te_db_type() == 'Oracle':
            is_run = QMessageBox.question(self, '提示信息', '是否确认创建当前页面输入的信息创建%s用户？' % self.get_te_db_type())
            if is_run == QMessageBox.StandardButton.Yes:
                self.print_to_te_text_browser('正在创建用户...')
                user = self.get_te_db_user()
                password = self.get_te_db_password()
                create_user_statement = 'create user %s IDENTIFIED BY %s' % (user, password)
                grant_privileges_statement = 'GRANT CREATE USER,DROP USER,ALTER USER,CREATE ANY VIEW,' \
                                             'DROP ANY VIEW,EXP_FULL_DATABASE,IMP_FULL_DATABASE,DBA,' \
                                             'CONNECT,RESOURCE,CREATE SESSION  TO %s' % user
                is_user_created, create_user_msg = oracle_run_sql(connect, create_user_statement)
                is_granted_privileges, grant_msg = oracle_run_sql(connect, grant_privileges_statement)

                if is_user_created and is_granted_privileges:
                    self.print_to_te_text_browser('%s\n用户：%s\n密码：%s' % (create_user_msg, user, password))
                    is_run = QMessageBox.question(self, '提示信息', 'Oracle用户创建完成，是否立即执行数据库初始化？')
                    if is_run == QMessageBox.StandardButton.Yes:
                        self.execute_init_sql()
                else:
                    self.print_to_te_text_browser('创建用户失败！\n%s' % create_user_msg)

        else:
            self.print_to_te_text_browser('用户取消初始化操作！')

    def check_env(self, db_type):
        result, path = get_sys_env_path(db_type)
        if result:
            self.run_init_sql()
        else:
            QMessageBox.warning(self, '提示信息', path)

    def execute_init_sql(self):
        if self.get_run_sql_connection_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.get_run_sql_db_connection_thread.db_type = self.get_te_db_type()
        self.get_run_sql_db_connection_thread.ip = self.get_te_db_ip().split(':')[0]
        self.get_run_sql_db_connection_thread.port = self.get_te_db_ip().split(':')[-1]
        self.get_run_sql_db_connection_thread.user = self.get_te_db_user()
        self.get_run_sql_db_connection_thread.password = self.get_te_db_password()
        self.get_run_sql_db_connection_thread.db = self.get_te_db_name()
        self.get_run_sql_connection_thread.start()
        self._start_get_run_sql_db_connection_thread.emit()

    def recheck_server(self):
        if self.get_te_db_type() == 'MySQL':
            self.print_to_te_text_browser('正在检查MySql服务是否已启动...')
            is_running, msg = check_service('mysql')
            # is_running = False
            # msg = ''
            if is_running:
                self.print_to_te_text_browser(msg)
                self.pre_run_init_sql()
            else:
                self.print_to_te_text_browser('MySql服务启动失败！')
                self.ui.pushButton_te_install_mysql.setEnabled(True)
        elif self.get_te_db_type() == 'Oracle':
            self.print_to_te_text_browser('正在检查Oracle服务是否已启动...')
            is_running, msg = check_service('oracleserviceorcl')
            # is_running = False
            # msg = ''
            if is_running:
                self.print_to_te_text_browser(msg)
                self.pre_run_init_sql()
            else:
                self.print_to_te_text_browser('Oracle服务启动失败！')
                self.ui.pushButton_te_install_mysql.setEnabled(True)

    def check_db_connection(self, is_init=False):
        if self.check_connection_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.ui.pushButton_te_db_test.setEnabled(False)
        self.check_db_connection_thread.db_type = self.get_te_db_type()
        self.check_db_connection_thread.ip = self.get_te_db_ip().split(':')[0]
        self.check_db_connection_thread.port = self.get_te_db_ip().split(':')[-1]
        self.check_db_connection_thread.user = self.get_te_db_user()
        self.check_db_connection_thread.password = self.get_te_db_password()
        self.check_db_connection_thread.db = self.get_te_db_name()
        self.check_db_connection_thread.is_init_check = is_init
        self.check_connection_thread.start()
        self._start_check_db_connection_thread.emit()

    def start_mysql_server(self):
        if self.server_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.server_thread.start()
        self._start_mysql_server_thread.emit()

    def start_oracle_server(self):
        if self.oracle_server_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        self.oracle_server_thread.start()
        self._start_oracle_server_thread.emit()

    def install_mysql(self):
        if self.init_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_te_text_browser('线程仍在运行，请耐心等待...')
            return
        is_run = QMessageBox.question(self, '提示信息', '检测到本机未安装MySql服务，是否立即安装？')
        if is_run == QMessageBox.StandardButton.Yes:
            # 先启动QThread子线程
            self.mysql_init_thread.unzip_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹")
            self.init_thread.start()
            # 发送信号，启动线程处理函数
            # 不能直接调用，否则会导致线程处理函数和主线程是在同一个线程，同样操作不了主界面
            self._start_mysql_init_thread.emit()
        else:
            self.mysql_init_thread.finished.emit()

    def lock_te_db_config_input(self):
        self.ui.comboBox_te_db_config_name.setEnabled(False)
        self.ui.comboBox_te_db_type.setEnabled(False)
        self.ui.lineEdit_te_db_ip.setEnabled(False)
        self.ui.lineEdit_te_db_user.setEnabled(False)
        self.ui.lineEdit_te_db_password.setEnabled(False)
        self.ui.lineEdit_te_db_name.setEnabled(False)
        self.ui.pushButton_te_db_test.setEnabled(False)
        self.ui.pushButton_te_install_mysql.setEnabled(False)

    def unlock_te_db_config_input(self):
        self.ui.comboBox_te_db_config_name.setEnabled(True)
        self.ui.comboBox_te_db_type.setEnabled(True)
        self.ui.lineEdit_te_db_ip.setEnabled(True)
        self.ui.lineEdit_te_db_user.setEnabled(True)
        self.ui.lineEdit_te_db_password.setEnabled(True)
        self.ui.lineEdit_te_db_name.setEnabled(True)
        self.ui.pushButton_te_db_test.setEnabled(True)
        self.ui.pushButton_te_install_mysql.setEnabled(True)

    def lock_be_db_config_input(self):
        self.ui.comboBox_be_db_config_name.setEnabled(False)
        self.ui.comboBox_be_db_type.setEnabled(False)
        self.ui.lineEdit_be_db_ip.setEnabled(False)
        self.ui.lineEdit_be_db_user.setEnabled(False)
        self.ui.lineEdit_be_db_password.setEnabled(False)
        self.ui.lineEdit_be_db_name.setEnabled(False)
        self.ui.pushButton_be_db_test.setEnabled(False)
        self.ui.pushButton_be_run_update_sql.setEnabled(False)

    def unlock_be_db_config_input(self):
        self.ui.comboBox_be_db_config_name.setEnabled(True)
        self.ui.comboBox_be_db_type.setEnabled(True)
        self.ui.lineEdit_be_db_ip.setEnabled(True)
        self.ui.lineEdit_be_db_user.setEnabled(True)
        self.ui.lineEdit_be_db_password.setEnabled(True)
        self.ui.lineEdit_be_db_name.setEnabled(True)
        self.ui.pushButton_be_db_test.setEnabled(True)
        self.ui.pushButton_be_run_update_sql.setEnabled(True)

    def get_te_db_config(self):
        db_config = []
        if self.get_te_db_type() == 'MySQL':
            db_config.append('hibernate.dialect=org.hibernate.dialect.MySQLDialect')
            db_config.append('validationQuery.sqlserver=SELECT 1')
            db_config.append(
                'jdbc.url=jdbc:mysql://%s/%s?useUnicode=true&characterEncoding=UTF-8' % (
                    self.get_te_db_ip(), self.get_te_db_name()))

        elif self.get_te_db_type() == 'Oracle':
            db_config.append('hibernate.dialect=org.hibernate.dialect.Oracle10gDialect')
            db_config.append('validationQuery.sqlserver=SELECT 1 FROM DUAL')
            db_config.append(
                'jdbc.url=jdbc:oracle:thin:@%s/%s' % (
                    self.get_te_db_ip(), self.get_te_db_name()))

        db_config.append('jdbc.username=%s' % self.get_te_db_user())
        db_config.append('jdbc.password=%s' % self.get_te_db_password())
        db_config.append('jdbc.dbType=%s' % self.get_te_db_type().lower())

        return db_config

    def start_modify(self):
        self.print_to_te_text_browser('开始修改环境配置...')
        t2_message = modify_file('%s/conf/Catalina/localhost/t2.xml' % self.get_te_tomcat_path(),
                                 '<Context docBase=',
                                 '<Context docBase="%s">' % self.get_te_program_path())
        self.print_to_te_text_browser(t2_message)
        # db_message = insert_to_index('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
        #                              self.get_te_db_config())
        if self.get_te_db_type() == 'MySQL':
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'hibernate.dialect=',
                        'hibernate.dialect=org.hibernate.dialect.MySQLDialect',
                        change_all=True)
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'validationQuery.sqlserver=',
                        'validationQuery.sqlserver=SELECT 1',
                        change_all=True)
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'jdbc.url=',
                        'jdbc.url=jdbc:mysql://%s/%s?useUnicode=true&characterEncoding=UTF-8' % (
                            self.get_te_db_ip(), self.get_te_db_name()),
                        change_all=True)
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'jdbc.username=',
                        'jdbc.username=%s' % self.get_te_db_user(),
                        change_all=True)
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'jdbc.password=',
                        'jdbc.password=%s' % self.get_te_db_password(),
                        change_all=True)
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'jdbc.dbType=',
                        'jdbc.dbType=%s' % self.get_te_db_type().lower(),
                        change_all=True)
        elif self.get_te_db_type() == 'Oracle':
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'hibernate.dialect=',
                        'hibernate.dialect=org.hibernate.dialect.Oracle10gDialect',
                        change_all=True)
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'validationQuery.sqlserver=',
                        'validationQuery.sqlserver=SELECT 1 FROM DUAL',
                        change_all=True)
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'jdbc.url=',
                        'jdbc.url=jdbc:oracle:thin:@%s/%s' % (self.get_te_db_ip(), self.get_te_db_name()),
                        change_all=True)
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'jdbc.username=',
                        'jdbc.username=%s' % self.get_te_db_user(),
                        change_all=True)
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'jdbc.password=',
                        'jdbc.password=%s' % self.get_te_db_password(),
                        change_all=True)
            modify_file('%s/WEB-INF/classes/config/dbconfig.properties' % self.get_te_program_path(),
                        'jdbc.dbType=',
                        'jdbc.dbType=%s' % self.get_te_db_type().lower(),
                        change_all=True)
        else:
            pass

        # self.print_to_te_text_browser(db_message)

        port_message = modify_file('%s/conf/server.xml' % self.get_te_tomcat_path(),
                                   'protocol="HTTP/1.1"',
                                   '    <Connector port="%s" protocol="HTTP/1.1"' % self.get_biz_port(),
                                   include_with=True)
        modify_file('%s/bin/setclasspath.bat' % self.get_te_tomcat_path(),
                    'set _RUNJAVA="%JRE_HOME%\\bin\\java.exe"',
                    'set _RUNJAVA="%JRE_HOME%\\bin\\javaw.exe"')
        self.print_to_te_text_browser(port_message)
        self.print_to_te_text_browser('文件修改完成，可执行T2启动！')

    def te_modify(self):
        self.print_to_te_text_browser('正在检测License...')
        if check_license(self.get_te_program_path()):
            self.print_to_te_text_browser('License文件已存在！')
            self.is_license_configured = True
            self.start_modify()
            self.save_te_path_config(self.configured_te_path_config)
            self.is_te_env_configured = True
            self.start_t2()
        else:
            self.print_to_te_text_browser('未找到License，请指定License文件路径！')
            self.child_license_select.show()

    def copy_license_file(self):
        copy_result = copy_file(self.child_license_select.get_current_text(),
                                '%s\\WEB-INF\\classes' % self.get_te_program_path())
        self.child_license_select.close()
        if copy_result:
            self.print_to_te_text_browser('License文件复制成功！')
            self.save_te_path_config(self.configured_te_path_config)
            self.is_te_env_configured = True
            self.start_t2()
        else:
            self.print_to_te_text_browser('License文件复制失败！')

    def print_to_te_text_browser(self, text):
        self.ui.textBrowser_te_logs.append(str(text))

    def select_te_program_path(self):
        te_program_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                                     self.ui.lineEdit_te_program_path.text())
        self.ui.lineEdit_te_program_path.setText(te_program_path)

    def select_te_tomcat_path(self):
        te_tomcat_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                                    self.ui.lineEdit_te_tomcat_path.text())
        self.ui.lineEdit_te_tomcat_path.setText(te_tomcat_path)

    def select_te_update_path(self):
        te_update_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                                    self.ui.lineEdit_te_update_path.text())
        self.ui.lineEdit_te_update_path.setText(te_update_path)

    # def select_te_jdk_path(self):
    #     te_jdk_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
    #                                                              self.ui.lineEdit_te_jdk_path.text())
    #     self.ui.lineEdit_te_jdk_path.setText(te_jdk_path)

    def select_te_structure_path(self):
        te_structure_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                                       self.ui.lineEdit_te_structure_path.text())
        self.ui.lineEdit_te_structure_path.setText(te_structure_path)

    def select_te_patch_path(self):
        te_patch_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                                   self.ui.lineEdit_te_patch_path.text())
        self.ui.lineEdit_te_patch_path.setText(te_patch_path)

    def clear_te_logs(self):
        self.ui.textBrowser_te_logs.clear()

    def clear_be_logs(self):
        self.ui.textBrowser_be_logs.clear()

    def get_biz_port(self):
        return self.ui.lineEdit_biz_port.text()

    def set_biz_port(self, text):
        self.ui.lineEdit_biz_port.setText(text)

    def get_update_port(self):
        return self.ui.lineEdit_update_port.text()

    def set_update_port(self, text):
        self.ui.lineEdit_update_port.setText(text)

    def get_te_structure_name(self):
        return self.ui.lineEdit_te_structure_name.text()

    def get_te_update_patch_name(self):
        return self.ui.lineEdit_te_patch_name.text()

    def get_te_db_type(self):
        return self.ui.comboBox_te_db_type.currentText()

    def set_te_db_type(self, text):
        self.ui.comboBox_te_db_type.setCurrentText(text)

    def get_te_db_name(self):
        return self.ui.lineEdit_te_db_name.text()

    def set_te_db_name(self, text):
        self.ui.lineEdit_te_db_name.setText(text)

    def get_te_db_ip(self):
        return self.ui.lineEdit_te_db_ip.text()

    def set_te_db_ip(self, text):
        return self.ui.lineEdit_te_db_ip.setText(text)

    def get_te_db_user(self):
        return self.ui.lineEdit_te_db_user.text()

    def set_te_db_user(self, text):
        return self.ui.lineEdit_te_db_user.setText(text)

    def get_te_db_password(self):
        return self.ui.lineEdit_te_db_password.text()

    def set_te_db_password(self, text):
        return self.ui.lineEdit_te_db_password.setText(text)

    def get_te_program_path(self):
        return self.ui.lineEdit_te_program_path.text()

    def set_te_program_path(self, text):
        return self.ui.lineEdit_te_program_path.setText(text)

    def get_te_tomcat_path(self):
        return self.ui.lineEdit_te_tomcat_path.text()

    def set_te_tomcat_path(self, text):
        return self.ui.lineEdit_te_tomcat_path.setText(text)

    # def get_te_jdk_path(self):
    #     return self.ui.lineEdit_te_jdk_path.text()
    #
    # def set_te_jdk_path(self, text):
    #     return self.ui.lineEdit_te_jdk_path.setText(text)

    def get_te_update_path(self):
        return self.ui.lineEdit_te_update_path.text()

    def set_te_update_path(self, text):
        return self.ui.lineEdit_te_update_path.setText(text)

    def get_te_structure_path(self):
        return self.ui.lineEdit_te_structure_path.text()

    def set_te_structure_path(self, text):
        return self.ui.lineEdit_te_structure_path.setText(text)

    def get_te_patch_path(self):
        return self.ui.lineEdit_te_patch_path.text()

    def set_te_patch_path(self, text):
        return self.ui.lineEdit_te_patch_path.setText(text)

    def check_be_db_connection(self):
        if not self.get_be_db_ip():
            self.print_to_be_text_browser('请输入主机/端口！')
        elif not check_url(self.get_be_db_ip()):
            self.print_to_be_text_browser('主机/端口输入格式不正确，请重新输入！\n例：127.0.0.1:3306')
        elif not self.get_be_db_name():
            self.print_to_be_text_browser('请输入数据库名称！')
        elif not self.get_be_db_user():
            self.print_to_be_text_browser('请输入用户名！')
        elif not self.get_be_db_password():
            self.print_to_be_text_browser('请输入密码！')
        else:
            self.check_be_db_connection_main()

    def check_be_db_connection_main(self):
        if self.check_be_connection_thread.isRunning():  # 如果该线程正在运行，则不再重新启动
            self.print_to_be_text_browser('线程仍在运行，请耐心等待...')
            return
        self.check_be_db_connection_thread.db_type = self.get_be_db_type()
        self.check_be_db_connection_thread.ip = self.get_be_db_ip().split(':')[0]
        self.check_be_db_connection_thread.port = self.get_be_db_ip().split(':')[-1]
        self.check_be_db_connection_thread.user = self.get_be_db_user()
        self.check_be_db_connection_thread.password = self.get_be_db_password()
        self.check_be_db_connection_thread.db = self.get_be_db_name()
        self.check_be_connection_thread.start()
        self._start_check_be_db_connection_thread.emit()

    def select_be_redis_path(self):
        be_redis_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                                   self.ui.lineEdit_be_redis_path.text())
        self.ui.lineEdit_be_redis_path.setText(be_redis_path)

    def select_be_server_path(self):
        be_server_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                                    self.ui.lineEdit_be_server_path.text())
        self.ui.lineEdit_be_server_path.setText(be_server_path)

    def select_be_client_path(self):
        be_client_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                                    self.ui.lineEdit_be_client_path.text())
        self.ui.lineEdit_be_client_path.setText(be_client_path)

    def select_be_logs_path(self):
        be_logs_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                                  self.ui.lineEdit_be_logs_path.text())
        self.ui.lineEdit_be_logs_path.setText(be_logs_path)

    def select_be_war_path(self):
        be_war_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                                 self.ui.lineEdit_be_war_path.text())
        self.ui.lineEdit_be_war_path.setText(be_war_path)

    # def select_be_jdk_path(self):
    #     be_jdk_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
    #                                                              self.ui.lineEdit_be_jdk_path.text())
    #     self.ui.lineEdit_be_jdk_path.setText(be_jdk_path)

    def delete_bank_config(self):
        if len(self.get_current_bank_config_items()):
            saved_bank_config_dict = read_yaml(r'.\data\saved_bank_conf.yml')
            if saved_bank_config_dict['data']['saved_bank_config']:
                saved_bank_config_dict['data']['saved_bank_config'].pop(self.get_current_bank_config_item())
                clear_yaml(r'.\data\saved_bank_conf.yml')
                write_yaml(r'.\data\saved_bank_conf.yml', saved_bank_config_dict)
                self.print_to_be_text_browser('当前配置已删除！')
                self.load_saved_bank_config()
                self.switch_current_bank_config()
        else:
            self.print_to_be_text_browser('无已保存的配置!')

    def load_saved_bank_config(self):
        try:
            self.ui.comboBox_be_db_config_name.clear()
            saved_bank_config_names = read_yaml(r'.\data\saved_bank_conf.yml')['data']['saved_bank_config']
            self.ui.comboBox_be_db_config_name.addItems([*saved_bank_config_names])
        except TypeError:
            return

    def switch_current_bank_config(self):
        saved_bank_config_dict = read_yaml(r'.\data\saved_bank_conf.yml')
        if saved_bank_config_dict:
            try:
                current_bank_config_details = \
                    saved_bank_config_dict['data']['saved_bank_config'][self.get_current_bank_config_item()][0]
                self.set_be_db_type(current_bank_config_details.get('db_type', ''))
                self.set_be_db_ip(current_bank_config_details.get('db_ip', ''))
                self.set_be_db_name(current_bank_config_details.get('db_name', ''))
                self.set_be_db_user(current_bank_config_details.get('db_user', ''))
                self.set_be_db_password(current_bank_config_details.get('db_password', ''))
                self.set_be_redis_path(current_bank_config_details.get('redis_path', ''))
                self.set_be_redis_port(current_bank_config_details.get('redis_port', ''))
                self.set_be_server_path(current_bank_config_details.get('server_path', ''))
                self.set_be_server_port(current_bank_config_details.get('server_port', ''))
                self.set_be_client_path(current_bank_config_details.get('client_path', ''))
                self.set_be_client_port(current_bank_config_details.get('client_port', ''))
                self.set_be_logs_path(current_bank_config_details.get('log_path', ''))
                self.set_be_war_path(current_bank_config_details.get('war_path', ''))
            except (TypeError, KeyError):
                return

    def show_be_save_db_config(self):
        self.child_be_save_db_config.show()
        self.child_be_save_db_config.set_default_text('%s - %s' % (self.get_be_db_type(), self.get_be_db_name()))

    def check_be_db_config(self):
        if not self.get_be_db_ip():
            self.print_to_be_text_browser('请输入主机/端口！')
        elif not check_url(self.get_be_db_ip()):
            self.print_to_be_text_browser('主机/端口输入格式不正确，请重新输入！\n例：127.0.0.1:3306')
        elif not self.get_be_db_name():
            self.print_to_be_text_browser('请输入数据库名称！')
        elif not self.get_be_db_user():
            self.print_to_be_text_browser('请输入用户名！')
        elif not self.get_be_db_password():
            self.print_to_be_text_browser('请输入密码！')
        else:
            self.show_be_save_db_config()

    def save_be_db_config_to_yml(self):
        save_bank_config(config_name=self.child_be_save_db_config.get_current_text(),
                         db_type=self.get_be_db_type(),
                         db_ip=self.get_be_db_ip(),
                         db_name=self.get_be_db_name(),
                         db_user=self.get_be_db_user(),
                         db_password=self.get_be_db_password(),
                         redis_path=self.get_be_redis_path(),
                         redis_port=self.get_be_redis_port(),
                         server_path=self.get_be_server_path(),
                         server_port=self.get_be_server_port(),
                         client_path=self.get_be_client_path(),
                         client_port=self.get_be_client_port(),
                         log_path=self.get_be_logs_path(),
                         war_path=self.get_be_war_path())
        if self.child_be_save_db_config.get_current_text() not in self.get_current_bank_config_items():
            self.ui.comboBox_be_db_config_name.addItem(self.child_be_save_db_config.get_current_text())
        self.ui.comboBox_be_db_config_name.setCurrentText(self.child_be_save_db_config.get_current_text())
        self.child_be_save_db_config.close()
        self.print_to_be_text_browser('当前配置保存成功！')

    def print_to_be_text_browser(self, text):
        self.ui.textBrowser_be_logs.append(str(text))

    def get_current_bank_config_item(self):
        return self.ui.comboBox_be_db_config_name.currentText()

    def set_current_bank_config_item(self, text):
        self.ui.comboBox_be_db_config_name.setCurrentText(text)

    def get_current_bank_type_item(self):
        return self.ui.comboBox_be_bank_type.currentText()

    def set_current_bank_type_item(self, text):
        self.ui.comboBox_be_bank_type.setCurrentText(text)

    def get_current_bank_config_items(self):
        current_items = []
        for i in range(self.ui.comboBox_be_db_config_name.count()):
            current_items.append(self.ui.comboBox_be_db_config_name.itemText(i))
        return current_items

    def get_be_db_type(self):
        return self.ui.comboBox_be_db_type.currentText()

    def set_be_db_type(self, text):
        self.ui.comboBox_be_db_type.setCurrentText(text)

    def get_be_db_name(self):
        return self.ui.lineEdit_be_db_name.text()

    def set_be_db_name(self, text):
        self.ui.lineEdit_be_db_name.setText(text)

    def get_be_db_ip(self):
        return self.ui.lineEdit_be_db_ip.text()

    def set_be_db_ip(self, text):
        self.ui.lineEdit_be_db_ip.setText(text)

    def get_be_db_user(self):
        return self.ui.lineEdit_be_db_user.text()

    def set_be_db_user(self, text):
        self.ui.lineEdit_be_db_user.setText(text)

    def get_be_db_password(self):
        return self.ui.lineEdit_be_db_password.text()

    def set_be_db_password(self, text):
        self.ui.lineEdit_be_db_password.setText(text)

    def get_be_redis_path(self):
        return self.ui.lineEdit_be_redis_path.text()

    def set_be_redis_path(self, text):
        self.ui.lineEdit_be_redis_path.setText(text)

    def get_be_redis_port(self):
        return self.ui.lineEdit_be_redis_port.text()

    def set_be_redis_port(self, text):
        self.ui.lineEdit_be_redis_port.setText(text)

    def get_be_server_path(self):
        return self.ui.lineEdit_be_server_path.text()

    def set_be_server_path(self, text):
        self.ui.lineEdit_be_server_path.setText(text)

    def get_be_server_port(self):
        return self.ui.lineEdit_be_server_port.text()

    def set_be_server_port(self, text):
        self.ui.lineEdit_be_server_port.setText(text)

    def get_be_client_path(self):
        return self.ui.lineEdit_be_client_path.text()

    def set_be_client_path(self, text):
        self.ui.lineEdit_be_client_path.setText(text)

    def get_be_client_port(self):
        return self.ui.lineEdit_be_client_port.text()

    def set_be_client_port(self, text):
        self.ui.lineEdit_be_client_port.setText(text)

    def get_be_logs_path(self):
        return self.ui.lineEdit_be_logs_path.text()

    def set_be_logs_path(self, text):
        self.ui.lineEdit_be_logs_path.setText(text)

    def get_be_war_path(self):
        return self.ui.lineEdit_be_war_path.text()

    def set_be_war_path(self, text):
        self.ui.lineEdit_be_war_path.setText(text)

    def get_be_bank_type(self):
        return self.ui.comboBox_be_bank_type.currentText()

    def set_be_bank_type(self, text):
        self.ui.comboBox_be_bank_type.setCurrentText(text)
