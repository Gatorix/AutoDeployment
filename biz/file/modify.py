import os
import chardet


def convert_all_slash(file_path):
    is_modified = False
    try:
        with open(file_path, 'rb') as f:
            tmp = chardet.detect(f.read())
        with open(file_path, 'r', encoding=tmp['encoding']) as f1, \
                open("%s.bak" % file_path, "w", encoding=tmp['encoding']) as f2:
            for line in f1:
                if line.endswith('\\'):
                    line = line.replace('\\', '/')
                    is_modified = True
                f2.write(line)
            os.remove(file_path)
            os.rename("%s.bak" % file_path, file_path)
            if is_modified:
                return '%s修改成功' % file_path.split('/')[-1]
            else:
                return '%s修改失败：未知错误' % file_path.split('/')[-1]
    except FileNotFoundError as ffe:
        return '%s修改失败：文件不存在！\n%s' % (file_path.split('/')[-1], ffe)
    except PermissionError as pe:
        return '%s修改失败：权限错误！\n%s' % (file_path.split('/')[-1], pe)
    except OSError as ose:
        return '%s修改失败：路径错误！\n%s' % (file_path.split('/')[-1], ose)


# print(convert_all_slash(r'D:\bank_env\bank2.0\Tomcat-client\webapps\bank\WEB-INF\classes\conf\sdb_new.properties'))


def modify_file(file_path: str, target_str: str, replace_str: str, change_all=False, include_with=False):
    is_modified = False
    try:
        if change_all:
            with open(file_path, "r", encoding="utf-8") as f1, open("%s.bak" % file_path, "w", encoding="utf-8") as f2:
                if include_with:
                    for line in f1:
                        if target_str in line:
                            line = '%s\n' % replace_str
                            is_modified = True
                        f2.write(line)
                else:
                    for line in f1:
                        if line.startswith(target_str):
                            line = '%s\n' % replace_str
                            is_modified = True
                        f2.write(line)
        else:
            # 只改第一个匹配行
            with open(file_path, "r", encoding="utf-8") as f1, open("%s.bak" % file_path, "w", encoding="utf-8") as f2:
                if include_with:
                    for line in f1:
                        if target_str in line:
                            if not is_modified:
                                line = '%s\n' % replace_str
                                is_modified = True
                        f2.write(line)
                else:
                    for line in f1:
                        if line.startswith(target_str):
                            if not is_modified:
                                line = '%s\n' % replace_str
                                is_modified = True
                        f2.write(line)

        os.remove(file_path)
        os.rename("%s.bak" % file_path, file_path)
        if is_modified:
            return '%s修改成功' % file_path.split('/')[-1]
        else:
            return '%s修改失败：未知错误' % file_path.split('/')[-1]
    except FileNotFoundError as ffe:
        return '%s修改失败：文件不存在\n%s' % (file_path.split('/')[-1], ffe)
    except OSError as ose:
        return '%s修改失败：路径错误\n%s' % (file_path.split('/')[-1], ose)


def insert_to_index(file_path: str, data: list, index=0):
    is_inserted = False
    try:
        with open(file_path, "r+", encoding="utf-8") as f:
            old_text = f.readlines()
            f.seek(index)
            for _ in data:
                f.write('%s\n' % _)
                is_inserted = True
            for old_lines in old_text:
                f.write(old_lines)
        if is_inserted:
            return '%s修改成功' % file_path.split('/')[-1]
        else:
            return '%s修改失败：未知错误' % file_path.split('/')[-1]
    except FileNotFoundError as ffe:
        return '%s修改失败：文件不存在\n%s' % (file_path.split('/')[-1], ffe)
    except OSError as ose:
        return '%s修改失败：路径错误\n%s' % (file_path.split('/')[-1], ose)

# test = 'test1111'
# print(test.startswith('test'))
# print(modify_file(r'D:\Tools\tomcat-build\tomcat-build\conf\Catalina\localhost\t2.xml', '<Context docBase=',
#                   '<Context docBase="D:\\Tools\\latest\\latest122211">'))
# t2.xml <Context docBase=
# print(insert_to_index(r'D:/Tools/latest/latest/WEB-INF/classes/config/dbconfig.properties',
#                       ['hibernate.dialect=org.hibernate.dialect.Oracle10gDialect',
#                        'validationQuery.sqlserver=SELECT 1',
#                        'jdbc.url=jdbc:mysql://127.0.0.1:3306/t2_cpv2?useUnicode=true&characterEncoding=UTF-8',
#                        'jdbc.username=root',
#                        'jdbc.password=root',
#                        'jdbc.dbType=mys121ql']))
# comment_config(r'D:/Tools/latest/latest/WEB-INF/classes/config/dbconfig.properties', '555')
