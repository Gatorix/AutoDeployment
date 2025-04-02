import pymysql
from pymysql import err
import cx_Oracle
from cx_Oracle import DatabaseError
import pymssql


def is_good_db_connection(db_type, host, port, user, password, database,sys_mode=False):
    if db_type == 'MySQL':
        try:
            connect = pymysql.Connect(host=host, port=int(port), user=user, password=password, database=database,
                                      charset='utf8', connect_timeout=1)
            connect.cursor()
            return True, '数据库连接成功！', connect
        except err.OperationalError as oe:
            return False, '数据库连接失败！\n%s' % oe, None

    elif db_type == 'Oracle':
        try:
            if sys_mode:
                connect = cx_Oracle.connect(user, password, '%s:%s/%s' % (host, port, database), mode=cx_Oracle.SYSDBA)
            else:
                connect = cx_Oracle.connect(user, password, '%s:%s/%s' % (host, port, database))
                connect.autocommit = True
            connect.cursor()
            return True, '数据库连接成功！', connect
        except DatabaseError as de:
            return False, '数据库连接失败！\n%s' % de, None
    elif db_type == 'SQLServer':
        try:
            connect = pymssql.connect(server=host, user=user, password=password, database=database,
                                      port=port, charset='cp936')
            connect.cursor(as_dict=True)
            return True, '数据库连接成功！', connect
        except pymssql.Error as pe:
            return False, '数据库连接失败！\n%s' % pe, None


#
#
# print(is_good_db_connection('MySQL', '192.168.5.249', '3306', 't2_cpv12352', 't2_cpv12352', ''))
#
# print(is_good_db_connection('Oracle', '127.0.0.1', '1521', 'sys', 'sys', 'ORCL', sys_mode=True))

# print(is_good_db_connection('SQLServer', '5555', '1521', 't2_cpv1_cp_jqcs', 't2_cpv1_cp_jqcs', 'ORCL'))
#
# str1='127.0.0.1:22:22'
# print(str1.split(':')[:-1])
# print(str1.split(':')[-2])
