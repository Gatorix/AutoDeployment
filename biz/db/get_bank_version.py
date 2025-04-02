from biz.db.connection_test import is_good_db_connection
from biz.db.run_sql import query_sql


def get_bank_name(db_type, host, port, user, password, database):
    result, msg, con = is_good_db_connection(db_type, host, port, user, password, database)
    if result:
        query_result, query_msg = query_sql(con.cursor(), 'select * From bis_bank_config')
        return result, msg, query_msg
    else:
        return result, msg, None


# print(get_bank_name('MySQL', '127.0.0.1', '3306', 'root', '123456', 't2_cpv2'))
