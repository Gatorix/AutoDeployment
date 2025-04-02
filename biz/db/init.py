import shutil
import os
from utils.cmd import cmd


def init_mysql(mysql_path):
    result = cmd('%s\\bin\\mysqld --initialize --console' % mysql_path)
    init_password = result[-16:-4]
    if 'Aborting' in result:
        return False, result
    else:
        return True, init_password


def move_mysql_ini(src_file, target_file):
    try:
        if not os.path.isfile(src_file):
            return False, "%s\n文件不存在" % src_file
        else:
            filepath, filename = os.path.split(target_file)
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            shutil.copyfile(src_file, target_file)
            return True, 'my.ini 文件复制成功'
    except PermissionError as pe:
        return False, pe

# r, w = move_my_ini(r'D:\Code\auto-deployment\data\resource\my.ini',
#                    r'D:\Code\mysql-5.7.36-winx64\mysql-5.7.36-winx64\bin\my.ini')
# print(w)
