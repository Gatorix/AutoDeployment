import os
import shutil
import chardet


def remove_temp_tree():
    if os.path.isdir('./data/temp/'):
        shutil.rmtree('./data/temp/')


def check_license(path):
    all_file_list = os.listdir('%s\\WEB-INF\\classes' % path)
    if [x for x in all_file_list if '.lic' in x]:
        return True
    else:
        return False


def get_sys_env_path(obj_name):
    obj_lower = obj_name.lower()
    abs_path = os.environ.get(obj_lower)
    if not abs_path:
        obj_path_list = [x for x in os.environ.get('path').split(';') if obj_lower in x]
        if len(obj_path_list) > 1:
            return True, obj_path_list[0]
        else:
            return False, '%s没有配置环境变量，请修改环境变量后重试！' % obj_lower
    else:
        return True, abs_path


def get_encoding(file):
    with open(file, 'rb') as f:
        tmp = chardet.detect(f.read())
        return tmp['encoding']


# print(get_encoding('C:\\Users\\caos\\Downloads\\V22040137\\sql\\V22040137_MYSQL.sql'))


def is_dir(path):
    return os.path.isdir(path)


def is_file(path):
    return os.path.isfile(path)


def get_all_filepath(folder, filetype='', is_all=False):
    """
    获取传入路径下所有满足条件的文件路径,如获取D:\\下所有的.log文件
    :param is_all:
    :param folder: 需查找的路径
    :param filetype: 需要过滤的文件类型
    :return: 满足条件的文件路径列表
    """
    file_type_len = len(filetype)
    file_path = []
    try:
        for f_path, dirs, fs in os.walk(folder):
            for f in fs:
                if '.DS_Store' in os.path.join(f_path, f):
                    pass
                elif is_all:
                    file_path.append(os.path.join(f_path, f))
                elif os.path.join(f_path, f)[-file_type_len:] != filetype:
                    pass
                else:
                    file_path.append(os.path.join(f_path, f))
    except TypeError:
        print('路径输入错误，检查后重新输入！')

    return file_path


def copy_file(src_file, target_path):
    if not os.path.isfile(src_file):
        return False
    else:
        path, name = os.path.split(src_file)  # 分离文件名和路径
        if not os.path.exists(target_path):
            os.makedirs(target_path)  # 创建路径
        shutil.copy(src_file, '%s\\%s' % (target_path, name))  # 复制文件
        return True


def get_structure_file_newest(temp_dir=r'.\data\temp'):
    original_structure_list = []
    base_structure_list = []
    split_key = '\\web\\'
    os.listdir(temp_dir)
    duplicate_files_count = 0
    for _ in os.listdir(temp_dir):
        original_structure_list.append(get_all_filepath('%s\\%s' % (temp_dir, _), is_all=True))
    for structure_pack_files in original_structure_list:
        if original_structure_list.index(structure_pack_files) == 0:
            base_structure_list.extend(structure_pack_files)
        else:
            extend_files_path = []
            base_files_path = []
            extend_files = []
            base_files = []
            for file_path in structure_pack_files:
                if split_key in file_path:
                    extend_files_path.append(file_path.split(split_key)[:-1])
                    extend_files.append(file_path.split(split_key)[-1])
            for file_path in base_structure_list:
                if split_key in file_path:
                    base_files_path.append(file_path.split(split_key)[:-1])
                    base_files.append(file_path.split(split_key)[-1])
            duplicate_files = set(base_files) & set(extend_files)
            duplicate_files_count += len(duplicate_files)
            if len(duplicate_files):
                # print('检测到%s个重复文件，比对最后修改时间...' % len(duplicate_files))
                for duplicate_file in duplicate_files:
                    complete_extend_file_path = '%s%s%s' % (
                        extend_files_path[extend_files.index(duplicate_file)][0], split_key, duplicate_file)
                    complete_base_file_path = '%s%s%s' % (
                        base_files_path[base_files.index(duplicate_file)][0], split_key, duplicate_file)
                    try:
                        if os.path.getmtime(complete_extend_file_path) > os.path.getmtime(complete_base_file_path):
                            base_structure_list.remove(complete_base_file_path)
                        else:
                            structure_pack_files.remove(complete_extend_file_path)
                    except ValueError:
                        pass
                base_structure_list.extend(structure_pack_files)
            else:
                base_structure_list.extend(structure_pack_files)
    if duplicate_files_count == 0:
        return base_structure_list, '检查完成！'
    else:
        return base_structure_list, '检查完成，共发现%s个重复文件，已替换最新版本！' % duplicate_files_count


def copy_structure_files_with_tree(file_list: list, target_dir: str, is_update=False):
    web_key = '\\web\\'
    sql_key = '\\sql\\'
    is_sql_exec = False
    if isinstance(file_list, list):
        if is_update:
            for file in file_list:
                if web_key in file:
                    copy_tree_core(file, target_dir, web_key, is_update=is_update)
            return True, '文件覆盖成功', None
        else:
            for file in file_list:
                if web_key in file:
                    copy_tree_core(file, target_dir, web_key)
                elif sql_key in file:
                    is_sql_exec = True
                    copy_tree_core(file, target_dir, sql_key)
            return True, '文件复制成功！', is_sql_exec
    else:
        return False, '文件列表格式不正确！', None


def copy_tree_core(file, target_dir, key, is_update=False):
    temp_dir = ''.join(file.split(key)[-1])
    if is_update:
        target_complete_dir = '%s\\%s' % (target_dir, '\\'.join(temp_dir.split('\\')[:-1]))
    else:
        target_complete_dir = '%s\\%s' % ('%s\\%s' % (target_dir, key[1:4]), '\\'.join(temp_dir.split('\\')[:-1]))
    target_complete_file_path = '%s\\%s' % (target_complete_dir, ''.join(file.split('\\')[-1]))
    if not os.path.isdir(target_complete_dir):
        try:
            os.makedirs(target_complete_dir)
        except FileExistsError as fee:
            return False, fee
    shutil.copyfile(file, target_complete_file_path)

# print('\\web\\'[1:4])
