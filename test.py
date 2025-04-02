import shutil

import cx_Oracle
from PyQt6 import QtCore, QtGui, QtWidgets

# import numpy as np


# from Distances import radial_distance
# def radial_distance(body1, body2, utc, ref, abcorr, obs):
#     x_1 = 1
#     x_2 = 4
#     y_1 = 5
#     y_2 = 2
#     z_1 = 7
#     z_2 = 6
#
#     d_rad = x_1 * x_2
#     return d_rad
#
#
# class Ui_window1(object):
#     def setupUi(self, window1):
#         window1.setObjectName("window1")
#         window1.resize(485, 530)  # 820 530
#         self.centralwidget = QtWidgets.QWidget(window1)
#         self.centralwidget.setObjectName("centralwidget")
#         window1.setCentralWidget(self.centralwidget)
#
#         self.groupBox_2 = QtWidgets.QGroupBox("groupBox_2", self.centralwidget)
#
#         self.output_rd = QtWidgets.QTextBrowser(self.groupBox_2)
#         self.output_rd.setGeometry(QtCore.QRect(10, 90, 331, 111))
#         self.output_rd.setObjectName("output_rd")
#
#         self.retranslateUi(window1)
#
#         QtCore.QMetaObject.connectSlotsByName(window1)
#
#     def retranslateUi(self, window1):
#         _translate = QtCore.QCoreApplication.translate
#         window1.setWindowTitle(_translate("window1", "GUI"))
#
#     def rad_distance(self):
#         time_rd = np.asarray([1, 2])  # ? (self.get_time_rd())
#
#         body1, body2 = ['EARTH', 'SUN']
#
#         rad_dis = radial_distance(body1, body2, time_rd, 'HCI', 'NONE', 'SUN')
#
#         #        self.output_rd.setText(rad_dis)
#         self.output_rd.append(str(rad_dis))  # + str
#
#
# #
# # ip = '127.0.0.1：3306'.split(':')[0]
# # port = '127.0.0.1:3306'.split(':')[-1]
# #
# # print(ip)
#
# def test(**configs):
#     # print(test)
#
#     data = {
#         'db_type': configs.get('aaa'),
#         'db_ip': configs.get('bbb')
#
#     }
#     print(data)
#
#
# test(aaa='vv000v', bbb='vvv')
import sys
from PyQt6 import QtCore, QtWidgets

from biz.db.connection_test import is_good_db_connection
from biz.db.init import init_mysql
from biz.db.run_sql import run_sql_by_cmd
from biz.file.config import read_yaml, get_bank_info
from biz.file.modify import modify_file, insert_to_index
from utils.cmd import cmd
from utils.net import get_patch, get_structure


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MyWindow')
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.button = QtWidgets.QPushButton('Do it')
        self.button.clicked.connect(self.my_method)
        layout = QtWidgets.QGridLayout(self._main)
        layout.addWidget(self.button)
        layout.addWidget(self.button)

    @QtCore.pyqtSlot()
    def my_method(self):
        self.n = 5
        self.loadthread = MyThread(self.n, self)
        self.loadthread.finished.connect(self.on_finished)
        self.loadthread.start()

    @QtCore.pyqtSlot()
    def on_finished(self):
        print('thread finished')


class MyThread(QtCore.QThread):
    def __init__(self, n, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.n = n

    def run(self):
        for i in range(self.n):
            print(i)
        print('cycle finished')


import subprocess as sp

if __name__ == '__main__':
    # app = QtWidgets.QApplication.instance()
    # if app is None:
    #     app = QtWidgets.QApplication(sys.argv)
    # mainGui = MyWindow()
    # mainGui.show()
    # # app.aboutToQuit.connect(app.deleteLater)
    # sys.exit(app.exec())

    # print(run_as_admin('cd D:\\mysql-5.7.36-winx64\\bin\nmysqld --install\nnet start mysql'))
    # print(run_as_admin('mysqld --install'))
    # print(cmd('mysqld --install'))
    # print(cmd('java -version'))

    # prog = sp.Popen(['runas', '/noprofile', '/user:Administrator', 'net start mysql'], stdin=sp.PIPE)
    # # prog.stdin.write('password')
    # prog.communicate()
    # from utils.cmd import run_as_admin, cmd
    #
    # print(run_as_admin('net start mysql\npause'))
    # from biz.db.connection_test import is_good_db_connection
    # from biz.file.file_path import get_all_filepath
    #
    # isgood, msg, con = is_good_db_connection('MySQL', '127.0.0.1', '3306', 't_user_20220517_crHU',
    #                                          't_user_20220517_crHU', 't_database_20220517_dbpa')
    # # print(con)
    #
    # all_sql_file = get_all_filepath(r'D:\Code\auto-deployment\data\resource\sql\init\mysql', '.sql')
    # # print(all_sql_file)
    # for sql_file in all_sql_file:
    # try:
    #     with open(sql_file, 'r+', encoding='utf8') as f:
    #         # every sql job last line marked;
    #         sql_list = f.read().split(';')[:-1]
    #         sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]
    # except UnicodeDecodeError:
    #     with open(sql_file, 'r+', encoding='gb2312') as f:
    #         # every sql job last line marked;
    #         sql_list = f.read().split(';')[:-1]
    #         sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]
    # for sql_item in sql_list:
    #     # print(sql_file)
    #     # print(sql_item)
    #
    #     try:
    #         effect_row = con.cursor().execute(sql_item)
    #         con.commit()
    #         print('effect rows is {}'.format(effect_row))
    #     except Exception as e:
    #         print(e)
    # print(all_sql_file.index(sql_file)+1,len(all_sql_file))
    # pass
    # saved_db_config_names = read_yaml(r'.\data\saved_db_conf.yml')
    # saved_db_config_names_list = [*saved_db_config_names]
    # print(saved_db_config_names)
    # removed_dict = saved_db_config_names['data']['saved_db_config'].pop('MySQL - t_database_202205517_HzVa99')
    # # removed_dict1 = saved_db_config_names['data']['saved_db_config']
    # print(removed_dict)
    # print(saved_db_config_names)
    # import jpype
    import os
    import time
    from biz.file.file_path import get_all_filepath, get_structure_file_newest, copy_structure_files_with_tree, \
        copy_file, get_sys_env_path
    from biz.file.unzip import un_zip

    # print(os.listdir('./data/temp'))
    # structures_name = os.listdir('./data/temp')
    # for _ in structures_name:
    #     print('正在解压%s...' % _)
    #     un_zip('./data/temp/%s' % _, './')

    # def check_structure_file_diff():
    #     base_dir_list = []
    # test = r'D:\Code\auto-deployment\test.bat'
    # mtime = os.path.getmtime(test)
    #
    # print(len(base_structure_list))
    # print((len(set(base_structure_list))))
    # structure_list, msg = get_structure_file_newest(r'D:\tmp\test')
    # print(msg)
    # # print(structure_list)
    # # print(get_all_filepath(r'.\data\temp\structure\'))
    # print(copy_structure_files_with_tree(structure_list, r'.\data\temp\structure'))
    # print(copy_structure_files_with_tree(get_all_filepath(r'.\data\temp\structure\web',is_all=True),
    #                                      r'D:\Tools\latest\latest2',is_update=True))
    # copy_file(r'D:\tmp\test\B20220500481.zip','.\\data\\temp')
    # from utils.net import get_patch,get_structure
    # print(get_patch('BFS.T3.4.0000.2021052101.Beta.zip'))
    # print(get_structure('B20220500142.zip'))
    # from biz.file.file_path import get_structure_file_newest
    #
    # # get_structure_file_newest()
    # from biz.file.modify import modify_file
    #
    # mysql_dialect = 'hibernate.dialect=org.hibernate.dialect.MySQLDialect'
    #
    # modify_file(r'D:\Tools\SYS_UPDATE\tomcat\conf\server.xml',
    #             '		   <Context path="" docBase=',
    #             '		   <Context path="" docBase="%s\\autoupdate1"')
    #
    # modify_file(r'D:\Tools\SYS_UPDATE\tomcat\conf\server.xml',
    #             '				 driverClassName=',
    #             '				 driverClassName="oracle.jdbc.driver.OracleDriver1"')
    #
    # modify_file(r'D:\Tools\SYS_UPDATE\tomcat\conf\server.xml',
    #             '				 url=',
    #             '				 url="jdbc:oracle:thin:@%s:%s:%s"')
    #
    # modify_file(r'D:\Tools\SYS_UPDATE\tomcat\conf\server.xml',
    #             '				 username=',
    #             '				 username="%s"')
    #
    # modify_file(r'D:\Tools\SYS_UPDATE\tomcat\conf\server.xml',
    #             '				 password=',
    #             '				 password="%s"/>')

    # driverClassName = "com.mysql.jdbc.Driver"
    # url = "jdbc:mysql://localhost:3306/t2_cpv2?useUnicode=true&amp;characterEncoding=utf8&amp;autoReconnect=true&amp;useSSL=false&amp;allowMultiQueries=true&amp;useServerPrepStmts=true&amp;rewriteBatchedStatements=true"
    # username = "t2_cpv2"
    # password = "root" / >
    #
    # driverClassName = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    # url = "jdbc:sqlserver://192.168.0.66:1433;DatabaseName=t2_cpv2_180925"
    # username = "sa"
    # password = "sasa" / >
    # print(cmd(r'D:\Tools\SYS_UPDATE\tomcat\bin\startup.bat'))
    # print(init_mysql(r'D:\tmp\test\mysql-5.7.36-winx64'))
    # print(get_patch())
    #
    import chardet

    # isgood, msg, con = is_good_db_connection('MySQL', '127.0.0.1', '3306', 't2_cpv11',
    #                                          't2_cpv11', 't2_cpv11')
    #
    # sql = 'C:\\Users\\caos\\Downloads\\V22040137\\sql\\V22040137_MYSQL.sql'
    # print(os.path.abspath('utils/net.py'))
    #
    #
    # def run_sql_by_cmd(user, password, database, sql_path, is_abs_mysql=False, mysql_path=''):
    #     mysql_cmd = 'mysql -u%s -p%s -D%s<%s' % (user, password, database, sql_path)
    #     abs_mysql_cmd = '%s -u%s -p%s -D%s<%s' % (mysql_path, user, password, database, sql_path)
    #     if is_abs_mysql:
    #         execute_result = cmd(abs_mysql_cmd)
    #     else:
    #         execute_result = cmd(mysql_cmd)
    #     return '\n'.join([x for x in execute_result.split('\n') if '[Warning]' not in x])
    #
    #
    # test = run_sql_by_cmd('root', '123456', 't2_cpv10', sql)
    # print(test)
    # print(cmd('mysql -uroot -p123456 -Dt2_cpv11<C:\\Users\\caos\\Downloads\\V22040137\\sql\\V22040137_MYSQL.sql'))
    # def get_encoding(file):
    #     with open(file, 'rb') as f:
    #         tmp = chardet.detect(f.read())
    #         return tmp['encoding']
    #
    #
    # error_count = 0
    # all_sql_file = get_all_filepath(r'.\data\resource\sql\init\mysql - 副本', '.sql')
    # # print(all_sql_file)
    # for sql_file in all_sql_file:
    #     print('正在执行第%s个文件，共%s个文件' % (all_sql_file.index(sql_file) + 1, len(all_sql_file)))
    #     # f = open(sql_file, 'rb')
    #     # print(chardet.detect(f.read()))
    #     # print(get_encoding(sql_file))
    #     try:
    #         # file = open(sql_file, 'r+', encoding='utf8')
    #         # lines = file.readlines()
    #         line_index = 0
    #         temp_str = ''
    #         temp_list = []
    #         final_list = []
    #         with open(sql_file, 'r+', encoding='utf8') as file:
    #             lines = file.readlines()
    #             for line in lines:
    #                 print(lines.index(line))
    #
    #                 print(line_index)
    #                 if line == '\n':
    #                     for _ in lines[line_index + 1:]:
    #                         if all([_ != '\n',
    #                                 not _.startswith('/*' or '--' or '#'),
    #                                 not _.endswith('*/')]):
    #                             temp_str += _.replace('\n', ' ')
    #                         else:
    #                             break
    #                     temp_list.append(temp_str)
    #                     print(temp_str)
    #                     temp_str = ''
    #                 else:
    #                     for _ in lines[line_index:]:
    #                         if all([_ != '\n',
    #                                 not _.startswith('/*' or '--' or '#'),
    #                                 not _.endswith('*/')]):
    #                             temp_str += _.replace('\n', ' ')
    #                         else:
    #                             break
    #                     temp_list.append(temp_str)
    #                     print(temp_str)
    #                     temp_str = ''
    #                 line_index += 1
    #             print(temp_list)
    #     #     # data = [i for i in open(sql_file, 'r+', encoding='utf8').read().split('\n')]
    #     #     # with open(sql_file, 'r+', encoding='utf8') as f:
    #     #     #     # 以两个\n行为标记
    #     #     #     # for line in f.read():
    #     #     #     #     if line == '\n':
    #     #     #     #         for _ in
    #     #     #     sql_list = f.read().split(';')[:-1]
    #     #     #     # if '/*' or '*/' not in sql_list:
    #     #     #     sql_list = [x.replace('\n', '') if '\n' in x else x for x in sql_list]
    #     except UnicodeDecodeError:
    #         with open(sql_file, 'r+', encoding='gb2312') as f:
    #             # every sql job last line marked;
    #             sql_list = f.read().split(';')[:-1]
    #             # if '/*' or '*/' not in sql_list:
    #             sql_list = [x.replace('\n', '') if '\n' in x else x for x in sql_list]
    # print(data)
    # for sql_item in sql_list:
    #     try:
    #         con.cursor().execute(sql_item)
    #         con.commit()
    #     except Exception as e:
    # self.signal.emit(str(sql_file))
    # self.signal.emit(str(sql_item))
    # self.signal.emit(str(e))
    # error_count += 1
    # print(get_structure('B20220500419'))
    # print(get_patch())
    # from biz.file.modify import modify_file
    #
    # modify_file(r'D:\Tools\SYS_UPDATE\tomcat\conf\server.xml',
    #             '    <Connector port=',
    #             '    <Connector port="9999" protocol="HTTP/1.1"'
    #             )
    # from utils.net import get_patch
    # get_patch()
    # print(cmd('netstat -ano|findstr "8080"'))
    # update_platform_path='D:\\Tools\\SYS_UPDATE'
    # db_info_config_file='%s\\tomcat\\conf\\server.xml' % update_platform_path
    # print(modify_file(db_info_config_file,
    #             '				 type="javax.sql.DataSource"',
    #             '				 driverClassName="com.mysql.jdbc.Driver"'))

    # test = [1, 1, 1, 1, 1, 1, 1, 1]
    # insert_to_index(r'D:\Tools\latest\latest2\WEB-INF\classes\config\dbconfig.properties', test,index=30)
    # run_sql_by_cmd('Oracle','t2','t2','orcl',)
    # print(cmd('sqlplus tester/tester @D:\\Code\\auto-deployment\\data\\resource\\sql\\init\\oracle\\03_create - 副本.sql'))
    # from biz.file.modify import modify_file
    # modify_file(r'C:\Users\caos\Downloads\server.xml','protocol="HTTP/1.1"',
    #                                                   '    <Connector port="9999" protocol="HTTP/1.1"',include_with=True)

    # is_connected, msg, con = is_good_db_connection('Oracle', '127.0.0.1', '1521', 't2', 't2', 'orcl')
    # try:
    #     con.cursor().execute('create user tester2 IDENTIFIED BY tester2')
    #     con.cursor().execute('GRANT CREATE USER,DROP USER,ALTER USER,CREATE ANY VIEW,DROP ANY VIEW,EXP_FULL_DATABASE,IMP_FULL_DATABASE,DBA,CONNECT,RESOURCE,CREATE SESSION  TO tester2')
    # except cx_Oracle.DatabaseError as cod:
    #     pass

    # print(get_sys_env_path('dbhome'))
    # print(cmd('echo exit | sqlplus tester2/tester2@192.168.5.249:1521/orcl @D:\\Code\\auto-deployment\\data\\resource\\sql\\init\\oracle\\10010009.sql'))

    # import win32api
    #
    #
    # def start():
    #     cmdd = r"D:\Code\auto-deployment\shell\oracle\run_sql.bat"
    #     win32api.ShellExecute(0, 'open', cmdd, '', '', 1)  # 前台打开
    # import datetime
    #
    # # print(datetime.date(datetime.now()))
    #
    # # cmd('echo exit | .\\shell\\tomcat\\start_update_platform.bat')
    # # os.system('.\\shell\\tomcat\\start_update_platform.bat')
    #
    # test1 = ['1', '2', '3']
    # test2 = ['4', '5', '6']
    #
    # pre = []
    # for i in range(len(test1)):
    #     # print(pre_data[i],interface[i])
    #     pre.append(str(test1[i]))
    #     pre.append(str(test2[i]))
    # print(pre)
    # print([''.join(x) for x in zip(pre[0::2], pre[1::2])])
    # from biz.file.config import read_yaml
    #
    #
    # def get_bank_info():
    #     bank_name = []
    #     bif_name = []
    #     bank_info = read_yaml(r'.\data\bank_info.yml')['bankInfo']
    #     for _ in bank_info:
    #         bank_name.append(_['bankName'])
    #         bif_name.append(_['bif_name'])
    #     return bank_name, bif_name
    #
    #
    # print(bank_name)
    # print(bif_name)
    copy_file(r'C:\Users\caos\Downloads\新银行接口所需资料_20190923(3)\新银行接口所需资料_20190923\新银行接口部署.docx',
              r'C:\Users\caos\Downloads\新银行接口所需资料_20190923(3)\新银行接口所需资料_20190923\服务平台')
    os.rename(
        r'C:\Users\caos\Downloads\新银行接口所需资料_20190923(3)\新银行接口所需资料_20190923\服务平台\新银行接口部署.docx',
        r'C:\Users\caos\Downloads\新银行接口所需资料_20190923(3)\新银行接口所需资料_20190923\服务平台\新银行接口部署.doc')
