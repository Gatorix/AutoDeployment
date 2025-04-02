import time
import zipfile
import os
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from biz.db.init import move_mysql_ini, init_mysql
from biz.db.run_sql import query_sql, run_sql_by_cmd
from biz.file.modify import modify_file
from biz.file.file_path import get_all_filepath, get_structure_file_newest, copy_structure_files_with_tree, copy_file, \
    get_encoding, remove_temp_tree
from biz.db import connection_test
from biz.file.unzip import un_zip
from utils.cmd import run_as_admin
from utils.net import get_structure, get_patch, port_is_used, open_browser
from utils.str_func import get_current_date


class MysqlInitThread(QtCore.QObject):
    #  通过类成员对象定义信号对象
    started = pyqtSignal()
    finished = pyqtSignal()
    signal = pyqtSignal(str)
    user = pyqtSignal(str)
    password = pyqtSignal(str)
    next_step = pyqtSignal()

    def __init__(self):
        super(MysqlInitThread, self).__init__()
        self.unzip_path = ''

    def run(self):
        self.started.emit()
        file_name = r'.\data\resource\mysql-5.7.36-winx64.zip'
        zip_file = zipfile.ZipFile(file_name)
        if os.path.isdir('%s/mysql-5.7.36-winx64' % self.unzip_path):
            del zip_file
            self.signal.emit(str('指定的目录中已存在mysql文件夹，请重新指定！'))
            self.finished.emit()
        else:
            # self.signal.emit(self.unzip_path)
            count = 0
            for names in zip_file.namelist():
                count += 1
                zip_file.extract(names, '%s/' % self.unzip_path)
                self.signal.emit('解压进度： %s -- %s' % ('%s%%' % round(count / len(zip_file.namelist()) * 100, 2), names))
            zip_file.close()
            self.signal.emit('解压完成')
            modify_file('%s\\data\\resource\\my.ini' % os.getcwd(),
                        'basedir=',
                        'basedir=%s/mysql-5.7.36-winx64' % self.unzip_path)

            modify_file('%s\\data\\resource\\my.ini' % os.getcwd(),
                        'datadir=',
                        'datadir=%s/mysql-5.7.36-winx64/data' % self.unzip_path)

            is_ini_moved, msg = move_mysql_ini('.\\data\\resource\\my.ini',
                                               '%s/mysql-5.7.36-winx64/bin/my.ini' % self.unzip_path)
            if is_ini_moved:
                self.signal.emit('%s: %s/mysql-5.7.36-winx64/bin' % (msg, self.unzip_path))
                self.signal.emit('正在执行MySql初始化...')
                # modify_file('%s\\shell\\mysql\\init_mysql.bat' % os.getcwd(),
                #             'cd',
                #             'cd %s/mysql-5.7.36-winx64/bin' % self.unzip_path)
                init_result, init_msg = init_mysql('%s\\mysql-5.7.36-winx64' % self.unzip_path)
                if init_result:
                    self.signal.emit('MySql初始化完成！')
                    self.signal.emit('数据库初始密码：%s' % init_msg)
                    self.user.emit('root')
                    self.password.emit(init_msg)
                    # self.password.emit('123456')
                    self.signal.emit('正在尝试启动MySql服务，请查看控制台窗口...')
                    # cmd('%s\\mysql-5.7.36-winx64\\bin\\mysqld --install' % self.unzip_path)
                    run_as_admin('cd %s/mysql-5.7.36-winx64/bin\nmysqld --install' % self.unzip_path)
                    run_as_admin('cd %s/mysql-5.7.36-winx64/bin\nnet start mysql' % self.unzip_path)
                    self.next_step.emit()
                else:
                    self.signal.emit('MySql初始化失败！\n%s' % init_msg)
                self.finished.emit()
            else:
                self.signal.emit('move my.ini failed:%s' % msg)
                self.finished.emit()


class StartMysqlThread(QtCore.QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    signal = pyqtSignal(str)

    def __init__(self):
        super(StartMysqlThread, self).__init__()

    def run(self):
        self.started.emit()
        self.signal.emit('正在尝试启动MySql服务，请等待命令行窗口执行结束后重新点击初始化按钮...')
        if run_as_admin('net start mysql'):
            self.finished.emit()


class StartOracleThread(QtCore.QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    signal = pyqtSignal(str)

    def __init__(self):
        super(StartOracleThread, self).__init__()

    def run(self):
        self.started.emit()
        self.signal.emit('正在尝试启动Oracle服务，请等待命令行窗口执行结束后重新点击初始化按钮...')
        if run_as_admin('net start oracleserviceorcl'):
            self.finished.emit()


class GetDBConnectionThread(QtCore.QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    signal = pyqtSignal(str)
    connect = pyqtSignal(object)
    result = pyqtSignal(bool)
    config = pyqtSignal(list)
    all = pyqtSignal(bool, str, object)

    def __init__(self):
        super(GetDBConnectionThread, self).__init__()
        self.user = ''
        self.password = ''
        self.ip = ''
        self.port = ''
        self.db_type = ''
        self.db = None
        self.tested_config = []
        self.is_sys = False

    def run(self):
        self.started.emit()
        is_connected, msg, con = \
            connection_test.is_good_db_connection(self.db_type,
                                                  self.ip,
                                                  self.port,
                                                  self.user,
                                                  self.password,
                                                  self.db,
                                                  sys_mode=self.is_sys)

        if is_connected:
            self.connect.emit(con)
            self.tested_config.clear()
            self.tested_config.append(self.db_type)
            self.tested_config.append('%s:%s' % (self.ip, self.port))
            self.tested_config.append(self.user)
            self.tested_config.append(self.password)
            self.tested_config.append(self.db)
            self.config.emit(self.tested_config)
            self.all.emit(is_connected, msg, con)
        else:
            self.all.emit(is_connected, msg, None)

        self.signal.emit(msg)
        self.result.emit(is_connected)
        self.finished.emit()


class CheckDBConnectionThread(QtCore.QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    signal = pyqtSignal(str)
    result = pyqtSignal(bool)
    config = pyqtSignal(list)
    init_result = pyqtSignal(bool)

    def __init__(self):
        super(CheckDBConnectionThread, self).__init__()
        self.user = ''
        self.password = ''
        self.ip = ''
        self.port = ''
        self.db_type = ''
        self.db = None
        self.tested_config = []
        self.is_init_check = False

    def run(self):
        self.started.emit()
        is_connected, msg, con = \
            connection_test.is_good_db_connection(self.db_type,
                                                  self.ip,
                                                  self.port,
                                                  self.user,
                                                  self.password,
                                                  self.db)
        if is_connected:
            self.tested_config.clear()
            self.tested_config.append(self.db_type)
            self.tested_config.append('%s:%s' % (self.ip, self.port))
            self.tested_config.append(self.user)
            self.tested_config.append(self.password)
            self.tested_config.append(self.db)
            self.config.emit(self.tested_config)
        self.signal.emit(msg)
        self.result.emit(is_connected)
        if self.is_init_check:
            self.init_result.emit(is_connected)
        self.finished.emit()


class RunInitSqlThread(QtCore.QObject):
    started = pyqtSignal()
    signal = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super(RunInitSqlThread, self).__init__()
        self.connect = None
        self.sql_path = ''
        self.user = ''
        self.password = ''
        self.ip = ''
        self.port = ''
        self.db_type = ''
        self.db = ''

    def run(self):
        self.started.emit()
        if self.db_type == 'MySQL':
            all_sql_file = get_all_filepath(r'.\data\resource\sql\init\mysql', '.sql')
            self.signal.emit('开始执行初始化sql...')
            if self.ip == '127.0.0.1':
                for sql_file in all_sql_file:
                    self.signal.emit('正在执行第%s个文件，共%s个文件...' % (all_sql_file.index(sql_file) + 1, len(all_sql_file)))
                    self.signal.emit('正在检查sql文件编码类型...')
                    sql_file_encoding = get_encoding(sql_file).replace('-', '')
                    result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file,
                                            character=sql_file_encoding)
                    self.signal.emit(result)
            else:
                for sql_file in all_sql_file:
                    self.signal.emit('正在执行第%s个文件，共%s个文件...' % (all_sql_file.index(sql_file) + 1, len(all_sql_file)))
                    self.signal.emit('正在检查sql文件编码类型...')
                    sql_file_encoding = get_encoding(sql_file).replace('-', '')
                    result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file,
                                            character=sql_file_encoding, is_remote=True, ip=self.ip, port=self.port)
                    self.signal.emit(result)
        elif self.db_type == 'Oracle':
            all_sql_file = get_all_filepath(r'.\data\resource\sql\init\oracle', '.sql')
            self.signal.emit('开始执行初始化sql...')
            if self.ip == '127.0.0.1':
                for sql_file in all_sql_file:
                    self.signal.emit('正在执行第%s个文件，共%s个文件...' % (all_sql_file.index(sql_file) + 1, len(all_sql_file)))
                    result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file)
                    self.signal.emit(result)
            else:
                for sql_file in all_sql_file:
                    self.signal.emit('正在执行第%s个文件，共%s个文件...' % (all_sql_file.index(sql_file) + 1, len(all_sql_file)))
                    result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file,
                                            is_remote=True, ip=self.ip, port=self.port)
                    self.signal.emit(result)

        self.signal.emit('初始化sql执行完成！')
        self.finished.emit()


class GetStructureThread(QtCore.QObject):
    signal = pyqtSignal(str)
    started = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super(GetStructureThread, self).__init__()
        self.is_db_tested = False
        self.structure_name = None
        self.structure_list = []

    def run(self):
        self.started.emit()
        if ',' in self.structure_name:
            self.structure_list = list(set(self.structure_name.split(',')))
            for _ in self.structure_list:
                self.signal.emit(
                    '正在下载%s，当前第%s个构建包，共%s个...' % (_,
                                                  self.structure_list.index(_) + 1,
                                                  len(self.structure_list)))
                result, msg = get_structure(_)
                self.signal.emit(msg)
            self.finished.emit()
        else:
            self.signal.emit('正在下载%s...' % self.structure_name)
            result, msg = get_structure(self.structure_name)
            self.signal.emit(msg)
            self.finished.emit()


class UpdateStructureThread(QtCore.QObject):
    signal = pyqtSignal(str)
    started = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super(UpdateStructureThread, self).__init__()
        self.un_zip_result = []
        self.program_path = ''
        self.user = ''
        self.password = ''
        self.ip = ''
        self.port = ''
        self.db_type = ''
        self.db = None
        self.is_db_tested = False
        # self.structure_path = ''

    def run(self):
        if self.is_db_tested:
            structures_name = os.listdir('./data/temp')
            for _ in structures_name:
                self.signal.emit('正在解压 %s...' % _)
                result, msg = un_zip('./data/temp/%s' % _, './data/temp')
                self.signal.emit('%s %s' % (_, msg))
                self.un_zip_result.append(result)
            if self.un_zip_result and all(self.un_zip_result):
                # if len(os.listdir('./data/temp')) > 1:
                self.signal.emit('正在检查程序文件...')
                structure_file_list, msg = get_structure_file_newest()
                self.signal.emit(msg)
                self.signal.emit('正在复制更新文件到临时目录...')
                copy_result, copy_msg, is_sql_exec = copy_structure_files_with_tree(structure_file_list,
                                                                                    '.\\data\\temp\\structure')
                self.signal.emit(copy_msg)
                self.signal.emit('检查是否需执行sql...')
                if is_sql_exec:
                    self.signal.emit('开始执行sql...')
                    all_sql_files = get_all_filepath(r'.\data\temp\structure\sql', filetype='.sql')
                    if self.db_type == 'MySQL':
                        mysql_files = [x for x in all_sql_files if 'mysql' in x.lower()]
                        if self.ip == '127.0.0.1':
                            for sql_file in mysql_files:
                                self.signal.emit(
                                    '正在执行第%s个文件，共%s个文件...' % (mysql_files.index(sql_file) + 1, len(mysql_files)))
                                self.signal.emit('正在检查sql文件编码类型...')
                                sql_file_encoding = get_encoding(sql_file).replace('-', '')
                                result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file,
                                                        character=sql_file_encoding)
                                self.signal.emit(result)
                        else:
                            for sql_file in mysql_files:
                                self.signal.emit(
                                    '正在执行第%s个文件，共%s个文件...' % (mysql_files.index(sql_file) + 1, len(mysql_files)))
                                self.signal.emit('正在检查sql文件编码类型...')
                                sql_file_encoding = get_encoding(sql_file).replace('-', '')
                                result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file,
                                                        character=sql_file_encoding, is_remote=True, ip=self.ip,
                                                        port=self.port)
                                self.signal.emit(result)

                    elif self.db_type == 'Oracle':
                        oracle_files = [x for x in all_sql_files if 'orcl' in x.lower()]
                        if self.ip == '127.0.0.1':
                            for sql_file in oracle_files:
                                self.signal.emit(
                                    '正在执行第%s个文件，共%s个文件...' % (oracle_files.index(sql_file) + 1, len(oracle_files)))
                                result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file)
                                self.signal.emit(result)
                        else:
                            for sql_file in oracle_files:
                                self.signal.emit(
                                    '正在执行第%s个文件，共%s个文件...' % (oracle_files.index(sql_file) + 1, len(oracle_files)))
                                result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file,
                                                        is_remote=True, ip=self.ip, port=self.port)
                                self.signal.emit(result)
                    else:
                        pass
                    self.signal.emit('构建包sql执行完成！')
                self.signal.emit('正在覆盖程序文件...')
                copy_result, copy_msg, is_sql_exec = copy_structure_files_with_tree(
                    get_all_filepath(r'.\data\temp\structure\web', is_all=True),
                    self.program_path, is_update=True)
                if copy_result:
                    self.signal.emit('构建包更新成功！\n本次共更新%s个构建包：%s' % (len(structures_name),
                                                                   ','.join([x[:-4] for x in structures_name])))
                else:
                    self.signal.emit('Unknown error!')
                remove_temp_tree()
            else:
                self.signal.emit('部分或全部构建包解压失败，请检查后重试！')
        else:
            self.signal.emit('数据库连接失败，请先执行数据库连接测试！')
        self.un_zip_result.clear()
        remove_temp_tree()
        self.finished.emit()


class GetPatchThread(QtCore.QObject):
    signal = pyqtSignal(str)
    started = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super(GetPatchThread, self).__init__()
        self.patch_name = ''

    def run(self):
        self.signal.emit('正在下载%s...' % self.patch_name)
        result, msg = get_patch(self.patch_name)
        self.signal.emit(msg)
        self.finished.emit()


class UpdatePatchThread(QtCore.QObject):
    signal = pyqtSignal(str)
    started = pyqtSignal()
    start_monitoring = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super(UpdatePatchThread, self).__init__()
        self.patch_name = ''
        self.update_platform_path = ''
        self.user = ''
        self.password = ''
        self.ip = ''
        self.port = ''
        self.db_type = ''
        self.db = ''
        self.is_port_tested = False
        self.tested_port = ''
        self.update_platform_port = ''

    def run(self):
        self.signal.emit('正在检查当前数据库版本信息...')
        is_connected, msg, con = \
            connection_test.is_good_db_connection(self.db_type,
                                                  self.ip,
                                                  self.port,
                                                  self.user,
                                                  self.password,
                                                  self.db)
        if is_connected:
            is_executed, msg = query_sql(con.cursor(), 'select bs_ver from version_current')
            if is_executed:
                all_patch_file = get_all_filepath('.\\data\\temp', is_all=True)
                if all_patch_file:
                    if int(msg[0].split('.')[4]) < int(all_patch_file[0].split('.')[5]):
                        self.signal.emit('数据库版本检查通过')
                        self.signal.emit('正在复制文件到升级工具补丁包路径...')
                        temp_patch_path = get_all_filepath('.\\data\\temp', is_all=True)
                        if len(temp_patch_path) == 1:
                            copy_file(temp_patch_path[0], '%s\\patches\\patch_now' % self.update_platform_path)
                            self.signal.emit('补丁包复制完成！')
                            remove_temp_tree()
                            self.signal.emit('正在配置升级工具...')
                            db_config_file = '%s\\autoupdate\\WEB-INF\\classes\\dbconfig.properties' \
                                             % self.update_platform_path
                            db_info_config_file = '%s\\tomcat\\conf\\server.xml' % self.update_platform_path
                            modify_file('%s\\tomcat\\bin\\setclasspath.bat' % self.update_platform_path,
                                        'set _RUNJAVA="%JRE_HOME%\\bin\\java.exe"',
                                        'set _RUNJAVA="%JRE_HOME%\\bin\\javaw.exe"')
                            if self.db_type == 'MySQL':
                                # 修改方言
                                mysql_dialect = 'hibernate.dialect=org.hibernate.dialect.MySQLDialect'
                                modify_file(db_config_file, 'hibernate.dialect=', mysql_dialect)
                                # 修改启动端口
                                modify_file(db_info_config_file,
                                            '    <Connector port="',
                                            '    <Connector port="%s" protocol="HTTP/1.1"' % self.update_platform_port)
                                # 修改数据库配置
                                modify_file(db_info_config_file,
                                            '		   <Context path="" docBase=',
                                            '		   <Context path="" docBase="%s\\autoupdate">'
                                            % self.update_platform_path,
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 driverClassName=',
                                            '				 driverClassName="com.mysql.jdbc.Driver"',
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 url=',
                                            '				 url="jdbc:mysql://%s:%s/%s?useUnicode=true&amp;'
                                            'characterEncoding=utf8&amp;autoReconnect=true&amp;'
                                            'useSSL=false&amp;allowMultiQueries=true&amp;useServerPrepStmts=true&amp;'
                                            'rewriteBatchedStatements=true"' % (
                                                self.ip, self.port, self.db),
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 username=',
                                            '				 username="%s"' % self.user,
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 password=',
                                            '				 password="%s"/>' % self.password,
                                            change_all=True)

                            elif self.db_type == 'Oracle':
                                oracle_dialect = 'hibernate.dialect=org.hibernate.dialect.OracleDialect'
                                modify_file(db_config_file, 'hibernate.dialect=', oracle_dialect)
                                modify_file(db_info_config_file,
                                            '    <Connector port="',
                                            '    <Connector port="%s" protocol="HTTP/1.1"' % self.update_platform_port)
                                modify_file(db_info_config_file,
                                            '		   <Context path="" docBase=',
                                            '		   <Context path="" docBase="%s\\autoupdate">' % self.update_platform_path,
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 driverClassName=',
                                            '				 driverClassName="oracle.jdbc.driver.OracleDriver"',
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 url=',
                                            '				 url="jdbc:oracle:thin:@%s:%s:%s"' % (
                                                self.ip, self.port, self.db),
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 username=',
                                            '				 username="%s"' % self.user,
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 password=',
                                            '				 password="%s"/>' % self.password,
                                            change_all=True)

                            else:
                                sqlserver_dialect = 'hibernate.dialect=org.hibernate.dialect.SQLServerDialect'
                                modify_file(db_config_file, 'hibernate.dialect=', sqlserver_dialect)
                                modify_file(db_info_config_file,
                                            '    <Connector port="',
                                            '    <Connector port="%s" protocol="HTTP/1.1"' % self.update_platform_port)
                                oracle_dialect = 'hibernate.dialect=org.hibernate.dialect.OracleDialect'
                                modify_file(db_config_file, 'hibernate.dialect=', oracle_dialect)

                                modify_file(db_info_config_file,
                                            '		   <Context path="" docBase=',
                                            '		   <Context path="" docBase="%s\\autoupdate">' % self.update_platform_path,
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 driverClassName=',
                                            '				 driverClassName="oracle.jdbc.driver.OracleDriver"',
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 url=',
                                            '				 url="jdbc:sqlserver://%s:%s;DatabaseName=%s"' % (
                                                self.ip, self.port, self.db),
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 username=',
                                            '				 username="%s"' % self.user,
                                            change_all=True)

                                modify_file(db_info_config_file,
                                            '				 password=',
                                            '				 password="%s"/>' % self.password,
                                            change_all=True)
                            self.db_type = ''
                            self.signal.emit('升级工具配置完成！')
                            self.signal.emit('正在启动升级工具tomcat，请查看tomcat窗口...')
                            modify_file('.\\shell\\tomcat\\start_update_platform.bat', 'cd',
                                        'cd %s\\tomcat\\bin' % self.update_platform_path)
                            self.start_monitoring.emit()
                            os.system('.\\shell\\tomcat\\start_update_platform.bat')
                            self.finished.emit()
                            # self.signal.emit('升级工具tomcat启动成功！')
                            # self.signal.emit('正在启动浏览器...')
                            #
                            # self.signal.emit('浏览器已启动，请转到浏览器手工执行补丁包升级操作！')
                        else:
                            self.signal.emit('找到多个补丁包，请检查后重试！')
                    else:
                        self.signal.emit('数据库版本检查不通过，当前数据库版本较新！')
                else:
                    self.signal.emit('未找到补丁包！')
            else:
                self.signal.emit('数据库版本检查失败，请确认当前数据库是否已执行初始化！')
        else:
            self.signal.emit(msg)
        remove_temp_tree()
        self.finished.emit()


class StartT2Thread(QtCore.QObject):
    signal = pyqtSignal(str)
    started = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super(StartT2Thread, self).__init__()
        self.tomcat_path = ''

    def run(self):
        self.signal.emit('正在启动t2，请查看tomcat窗口！')
        modify_file('.\\shell\\tomcat\\start_t2.bat', 'cd',
                    'cd %s/bin' % self.tomcat_path)
        self.started.emit()
        os.system('.\\shell\\tomcat\\start_t2.bat')
        self.finished.emit()


class PortCheckThread(QtCore.QObject):
    signal = pyqtSignal(str)
    finished = pyqtSignal()
    is_biz_port_tested = pyqtSignal(bool)
    is_update_port_tested = pyqtSignal(bool)

    def __init__(self):
        super(PortCheckThread, self).__init__()
        self.biz_port = ''
        self.update_port = ''

    def run(self):
        if self.biz_port:
            self.check_biz_port()
        elif self.update_port:
            self.check_update_port()
        self.finished.emit()

    def check_biz_port(self):
        self.signal.emit('正在检测业务系统端口...')
        biz_is_used, biz_msg = port_is_used(self.biz_port)
        self.signal.emit('业务系统端口占用情况：%s' % biz_msg)
        if biz_is_used:
            self.is_biz_port_tested.emit(biz_is_used)
        self.biz_port = ''

    def check_update_port(self):
        self.signal.emit('正在检测升级工具端口...')
        update_is_used, update_msg = port_is_used(self.update_port)
        self.signal.emit('升级工具端口占用情况：%s' % update_msg)
        if update_is_used:
            self.is_update_port_tested.emit(update_is_used)
        self.update_port = ''


class TomcatMonitorThread(QtCore.QObject):
    signal = pyqtSignal(str)
    update_started = pyqtSignal(str)
    biz_1_started = pyqtSignal(str)
    biz_2_started = pyqtSignal(str)
    biz_3_started = pyqtSignal(str)
    biz_4_started = pyqtSignal(str)
    biz_5_started = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super(TomcatMonitorThread, self).__init__()
        self.path = ''
        self.port = ''
        self.url = ''
        self.tab_type = ''
        self.flag = False
        self.is_stop = False

    def run(self):
        self.signal.emit('正在监控日志文件...')
        log_file = '%s/logs/catalina.%s.log' % (self.path, get_current_date())
        if self.tab_type == 'update':
            if os.path.isfile(log_file):
                self.update_started.emit(log_file)
                self.monitor_core(log_file, self.flag)
            else:
                self.update_started.emit(log_file)
                create_log_file = open(log_file, 'w', encoding='gb2312')
                create_log_file.flush()
                create_log_file.close()
                self.monitor_core(log_file, self.flag)
        elif self.tab_type == 'biz_1':
            if os.path.isfile(log_file):
                self.biz_1_started.emit(log_file)
                self.monitor_core(log_file, self.flag)
            else:
                self.biz_1_started.emit(log_file)
                create_log_file = open(log_file, 'w', encoding='gb2312')
                create_log_file.flush()
                create_log_file.close()
                self.monitor_core(log_file, self.flag)
        elif self.tab_type == 'biz_2':
            if os.path.isfile(log_file):
                self.biz_2_started.emit(log_file)
                self.monitor_core(log_file, self.flag)
            else:
                self.biz_2_started.emit(log_file)
                create_log_file = open(log_file, 'w', encoding='gb2312')
                create_log_file.flush()
                create_log_file.close()
                self.monitor_core(log_file, self.flag)
        elif self.tab_type == 'biz_3':
            if os.path.isfile(log_file):
                self.biz_3_started.emit(log_file)
                self.monitor_core(log_file, self.flag)
            else:
                self.biz_3_started.emit(log_file)
                create_log_file = open(log_file, 'w', encoding='gb2312')
                create_log_file.flush()
                create_log_file.close()
                self.monitor_core(log_file, self.flag)
        self.finished.emit()
        self.reset_thread()

    def monitor_core(self, log_file, flag):
        with open(log_file, 'r', encoding='gb2312') as log:
            current_line_index = len(log.readlines())
        while True:
            if self.is_stop:
                break
            with open(log_file, 'r', encoding='gb2312') as log:
                for line in log.readlines()[current_line_index:]:
                    if 'Server startup' in line:
                        self.flag = True
                        break
            time.sleep(0.5)
            if self.flag:
                self.signal.emit('Tomcat启动成功！')
                self.signal.emit('正在尝试启动浏览器...')
                open_browser('http://127.0.0.1:%s%s' % (self.port, self.url))
                self.finished.emit()
                self.reset_thread()
                return

    def reset_thread(self):
        self.path = ''
        self.port = ''
        self.url = ''
        self.tab_type = ''
        self.flag = False
        self.is_stop = False


class LogPrintThread(QtCore.QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    signal = pyqtSignal(str, str)

    def __init__(self):
        super(LogPrintThread, self).__init__()
        self.is_stop = False
        self.current_env = ''
        self.log_file = ''
        self.tomcat_path = ''

    def run(self):
        self.started.emit()
        with open(self.log_file, 'r', encoding='gb2312') as log:
            current_line_index = len(log.readlines())
        if self.current_env != 'update':
            with open('%s/BytterLogs/error/bytter_error.log' % self.tomcat_path, 'r', encoding='utf8') as error_log:
                current_error_line_index = len(error_log.readlines())
        while True:
            if self.is_stop:
                break
            with open(self.log_file, 'r', encoding='gb2312') as log:
                for line in log.readlines()[current_line_index:]:
                    self.signal.emit(self.current_env, line)
                    current_line_index += 1
            if self.current_env != 'update':
                with open('%s/BytterLogs/error/bytter_error.log' % self.tomcat_path, 'r', encoding='utf8') as error_log:
                    for line in error_log.readlines()[current_error_line_index:]:
                        self.signal.emit(self.current_env, line)
                        current_error_line_index += 1
            time.sleep(0.5)
        self.finished.emit()
        self.is_stop = False
        self.current_env = ''
        self.log_file = ''


class BankUpdateThread(QtCore.QObject):
    signal = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super(BankUpdateThread, self).__init__()
        self.user = ''
        self.password = ''
        self.ip = ''
        self.port = ''
        self.db_type = ''
        self.db = None
        self.is_db_tested = False

    def run(self):
        if self.is_db_tested:
            self.signal.emit('开始执行sql...')
            all_sql_files = get_all_filepath(r'.\data\resource\sql\update', filetype='.sql')
            if self.db_type == 'MySQL':
                mysql_files = [x for x in all_sql_files if 'mysql' in x.lower()]
                if self.ip == '127.0.0.1':
                    for sql_file in mysql_files:
                        self.signal.emit(
                            '正在执行第%s个文件，共%s个文件...' % (mysql_files.index(sql_file) + 1, len(mysql_files)))
                        self.signal.emit('正在检查sql文件编码类型...')
                        sql_file_encoding = get_encoding(sql_file).replace('-', '')
                        result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file,
                                                character=sql_file_encoding)
                        self.signal.emit(result)
                else:
                    for sql_file in mysql_files:
                        self.signal.emit(
                            '正在执行第%s个文件，共%s个文件...' % (mysql_files.index(sql_file) + 1, len(mysql_files)))
                        self.signal.emit('正在检查sql文件编码类型...')
                        sql_file_encoding = get_encoding(sql_file).replace('-', '')
                        result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file,
                                                character=sql_file_encoding, is_remote=True, ip=self.ip,
                                                port=self.port)
                        self.signal.emit(result)

            elif self.db_type == 'Oracle':
                oracle_files = [x for x in all_sql_files if 'oracle' in x.lower()]
                if self.ip == '127.0.0.1':
                    for sql_file in oracle_files:
                        self.signal.emit(
                            '正在执行第%s个文件，共%s个文件...' % (oracle_files.index(sql_file) + 1, len(oracle_files)))
                        result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file)
                        self.signal.emit(result)
                else:
                    for sql_file in oracle_files:
                        self.signal.emit(
                            '正在执行第%s个文件，共%s个文件...' % (oracle_files.index(sql_file) + 1, len(oracle_files)))
                        result = run_sql_by_cmd(self.db_type, self.user, self.password, self.db, sql_file,
                                                is_remote=True, ip=self.ip, port=self.port)
                        self.signal.emit(result)
            else:
                pass
            self.signal.emit('银行接口升级sql执行完成！')
        else:
            self.signal.emit('数据库连接失败，请先执行数据库连接测试！')
        self.finished.emit()


class UnzipWarPackageThread(QtCore.QObject):
    signal = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super(UnzipWarPackageThread, self).__init__()
        self.war_path = ''
        self.client_path = ''
        self.server_path = ''

    def run(self):
        all_war_path = get_all_filepath(self.war_path, '.war')
        if len(all_war_path) == 2:
            for _ in all_war_path:
                if 'bankplatform' and '.war' in _:
                    self.signal.emit('正在复制%s' % _.split('\\')[-1])
                    copy_file(_, '%s/webapps' % self.server_path)
                    os.rename('%s/webapps/%s' % (self.server_path, _.split('\\')[-1]),
                              '%s/webapps/%s' % (self.server_path, _.split('\\')[-1].replace('.war', '.zip')))
                    self.signal.emit('正在解压%s，请稍后...' % _.split('\\')[-1])
                    unzip_result, msg = un_zip(
                        '%s/webapps/%s' % (self.server_path, _.split('\\')[-1].replace('.war', '.zip')),
                        '%s/webapps' % self.server_path, is_direct_unzip=True, folder_name='bankplatform')
                    self.signal.emit(msg)
                elif 'bankfront' and '.war' in _:
                    self.signal.emit('正在复制%s' % _.split('\\')[-1])
                    copy_file(_, '%s/webapps' % self.client_path)
                    os.rename('%s/webapps/%s' % (self.client_path, _.split('\\')[-1]),
                              '%s/webapps/%s' % (self.client_path, _.split('\\')[-1].replace('.war', '.zip')))
                    self.signal.emit('正在解压%s，请稍后...' % _.split('\\')[-1])
                    unzip_result, msg = un_zip(
                        '%s/webapps/%s' % (self.client_path, _.split('\\')[-1].replace('.war', '.zip')),
                        '%s/webapps' % self.client_path, is_direct_unzip=True, folder_name='bank')
                    self.signal.emit(msg)
                else:
                    self.signal.emit('未找到符合条件的war包！')
        elif len(all_war_path) > 2:
            self.signal.emit('War包路径下找到三个或更多War包，请仅保留两个：\n'
                             'bytter-bankplatform-build.war --服务平台端\n'
                             'bytter-bankfront-build.war --客户端')
        else:
            self.signal.emit('War包路径下未找到或仅有一个符合条件的War包，请把服务平台和客户端的war包放在同一目录下！')
        self.finished.emit()
