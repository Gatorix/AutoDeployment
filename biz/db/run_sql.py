import cx_Oracle
import pymysql.err
from utils.cmd import cmd


def query_sql(cursor, sql):
    try:
        cursor.execute(sql)
        return True, cursor.fetchall()[0]
    except pymysql.err.ProgrammingError as pepe:
        return False, pepe
    except cx_Oracle.DatabaseError as cod:
        return False, cod


def mysql_run_sql(connect, sql):
    try:
        connect.cursor().execute(sql)
        return True, '%s\n执行成功！' % sql
    except pymysql.err.ProgrammingError as pee:
        return False, '执行失败！\n%s' % pee
    except pymysql.err.OperationalError as pee:
        return False, '执行失败！\n%s' % pee


def oracle_run_sql(connect, sql):
    try:
        connect.cursor().execute(sql)
        return True, '%s\n执行成功！' % sql
    except cx_Oracle.DatabaseError as cod:
        return False, '执行失败！\n%s' % cod


def run_sql_by_cmd(db_type, user, password, database, sql_path,
                   character='utf8', is_remote=False, ip='', port=''):
    if is_remote:
        mysql_cmd = 'mysql -h%s -P%s -u%s -p%s -D%s<%s  --default-character-set=%s' % (
            ip, port, user, password, database, sql_path, character)
        oracle_cmd = 'sqlplus %s/%s@%s:%s/%s @%s' % (user, password, ip, port, database, sql_path)
    else:
        mysql_cmd = 'mysql -u%s -p%s -D%s<%s  --default-character-set=%s' % (
            user, password, database, sql_path, character)
        oracle_cmd = 'sqlplus %s/%s@%s @%s' % (user, password, database, sql_path)

    if db_type == 'MySQL':
        execute_result = cmd(mysql_cmd)
        return '\n'.join([x for x in execute_result.split('\n') if '[Warning]' not in x])
    elif db_type == 'Oracle':
        execute_result = cmd('echo exit | %s' % oracle_cmd)
        return '\n'.join([x for x in execute_result.split('\n') if '错误' not in x])
    elif db_type == 'SQLServer':
        return

# def create_user(connect):
#     user = 't_user_%s_%s' % (datetime.datetime.now().strftime('%Y%m%d'), random_str())
#     create_user_statement = "create user '%s'@'%%' identified by '%s';" % (user, user)
#     grant_privileges_statement = "grant all privileges on *.* to '%s'@'%%';" % user
#     try:
#         connect.cursor().execute(create_user_statement)
#         connect.cursor().execute(grant_privileges_statement)
#         return True, '用户创建成功！', user
#     except pymysql.err.ProgrammingError as pee:
#         return False, '用户创建失败！\n%s' % pee, None
#     except pymysql.err.OperationalError as pee:
#         return False, '用户创建失败！\n%s' % pee, None
#
#
# def create_database(connect):
#     database_name = 't_database_%s_%s' % (datetime.datetime.now().strftime('%Y%m%d'), random_str())
#     create_database_statement = "create database %s character set utf8;" % database_name
#     try:
#         connect.cursor().execute(create_database_statement)
#         return True, '数据库创建成功！', database_name
#     except pymysql.err.ProgrammingError as pee:
#         return False, '数据库创建失败！\n%s' % pee, None
#     except pymysql.err.OperationalError as pee:
#         return False, '数据库创建失败！\n%s' % pee, None


# is_good, msg, con = connection_test.is_good_db_connection('MySQL', '127.0.0.1', '3306', 'root', 'root', None)
#
# print(change_init_password(con))

# is_good, msg, con = connection_test.is_good_db_connection('MySQL', '127.0.0.1', '3306', 'root', 'root', 't2_cpv2')
# # print(connection_test.is_good_db_connection('MySQL', '127.0.0.1', '3306', 'root', 'root', 't2_cpv2'))
# print(cur)
# print(query_sql(cur, 'select * from version_current'))
