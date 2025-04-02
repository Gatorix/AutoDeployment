import os
import yaml


def get_current_path():
    return os.getcwd()


def write_yaml(file_path, yml_data):
    """
    根据跟定的yml数据，转换成yml文件
    :param file_path: yml文件路径
    :param yml_data: 需转换的字典数据
    :return: 无
    """
    file = open(file_path, 'a', encoding='utf-8')
    yaml.dump(yml_data, file, default_flow_style=False, sort_keys=False, allow_unicode=True)
    # 关闭文件
    file.close()


def read_yaml(file_path):
    """
    读取yml文件内容
    :param file_path: yml文件路径
    :return: 返回字典
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        yml_data = yaml.safe_load(f)
        # print(data['test_case'])
        f.close()
        return yml_data


def clear_yaml(file_path):
    """
    清空yml文件
    :param file_path: yml文件路径
    :return:
    """
    with open(file_path, 'r+', encoding='utf-8') as f:
        f.truncate()
        f.close()


def get_bank_info():
    bank_info_kv = {}
    bank_info = read_yaml(r'.\data\bank_info.yml')['bankInfo']
    for _ in bank_info:
        bank_info_kv[_['bankName']] = _['bif_name']
    return bank_info_kv


def save_bank_config(**configs):
    yml_path = '%s\\data\\saved_bank_conf.yml' % os.getcwd()
    # yml_path = r'D:\Code\auto-deployment\data\saved_db_conf.yml'
    try:
        read_yaml(yml_path)
    except FileNotFoundError as ffe:
        return ffe
    if_ele = {
        'data': {
            'saved_bank_config': {
                configs.get('config_name'): [{
                    'db_type': configs.get('db_type', ''),
                    'db_ip': configs.get('db_ip', ''),
                    'db_name': configs.get('db_name', ''),
                    'db_user': configs.get('db_user', ''),
                    'db_password': configs.get('db_password', ''),
                    'redis_path': configs.get('redis_path', ''),
                    'redis_port': configs.get('redis_port', ''),
                    'server_path': configs.get('server_path', ''),
                    'server_port': configs.get('server_port', ''),
                    'client_path': configs.get('client_path', ''),
                    'client_port': configs.get('client_port', ''),
                    'log_path': configs.get('log_path', ''),
                    'war_path': configs.get('war_path', ''),
                }]
            }
        }
    }

    previous_data = read_yaml(yml_path)
    if previous_data is not None:
        for key in if_ele['data']['saved_bank_config']:
            if not isinstance(if_ele['data'].get(key), list):
                if if_ele['data'].get(key) == previous_data['data'].get(key):
                    previous_data['data']['saved_bank_config'].update(if_ele['data']['saved_bank_config'])
        clear_yaml(yml_path)
        write_yaml(yml_path, previous_data)
    else:
        write_yaml(yml_path, if_ele)


def save_db_config(**configs):
    yml_path = '%s\\data\\saved_db_conf.yml' % os.getcwd()
    # yml_path = r'D:\Code\auto-deployment\data\saved_db_conf.yml'
    try:
        read_yaml(yml_path)
    except FileNotFoundError as ffe:
        return ffe
    if_ele = {
        'data': {
            'saved_db_config': {
                configs.get('config_name'): [{
                    'db_type': configs.get('db_type', ''),
                    'db_ip': configs.get('db_ip', ''),
                    'db_name': configs.get('db_name', ''),
                    'db_user': configs.get('db_user', ''),
                    'db_password': configs.get('db_password', ''),
                    'program_path': configs.get('program_path', ''),
                    'tomcat_path': configs.get('tomcat_path', ''),
                    'biz_port': configs.get('biz_port', ''),
                    'update_path': configs.get('update_path', ''),
                    'update_port': configs.get('update_port')
                }]
            }
        }
    }

    previous_data = read_yaml(yml_path)
    if previous_data is not None:
        for key in if_ele['data']['saved_db_config']:
            if not isinstance(if_ele['data'].get(key), list):
                if if_ele['data'].get(key) == previous_data['data'].get(key):
                    previous_data['data']['saved_db_config'].update(if_ele['data']['saved_db_config'])
        clear_yaml(yml_path)
        write_yaml(yml_path, previous_data)
    else:
        write_yaml(yml_path, if_ele)


# save_db_config(config_name='11395533',
# db_type='222', db_ip='33773', db_name='na--me', db_user='user', db_password='pass')


def save_config(**configs):
    yml_path = '%s\\data\\saved_ui_conf.yml' % os.getcwd()
    try:
        read_yaml(yml_path)
    except FileNotFoundError as ffe:
        return ffe
    if_ele = {
        'data': {
            't2': {
                'db': {
                    't2_db_conf_name': configs.get('t2_db_conf_name', ''),
                    't2_db_type': configs.get('t2_db_type', ''),
                    't2_db_ip': configs.get('t2_db_ip', ''),
                    't2_db_name': configs.get('t2_db_name', ''),
                    't2_db_user': configs.get('t2_db_user', ''),
                    't2_db_password': configs.get('t2_db_password', '')
                },
                'path': {
                    't2_program_path': configs.get('t2_program_path', ''),
                    't2_tomcat_path': configs.get('t2_tomcat_path', ''),
                    't2_update_path': configs.get('t2_update_path', ''),
                    't2_biz_port': configs.get('t2_biz_port', ''),
                    't2_update_port': configs.get('t2_update_port', ''),
                }
            },
            'bank': {
                'db': {
                    'bank_db_type': configs.get('bank_db_type', ''),
                    'bank_db_ip': configs.get('bank_db_ip', ''),
                    'bank_db_name': configs.get('bank_db_name', ''),
                    'bank_db_user': configs.get('bank_db_user', ''),
                    'bank_db_password': configs.get('bank_db_password', '')
                },
                'path': {
                    'bank_redis_path': configs.get('bank_redis_path', ''),
                    'bank_redis_port': configs.get('bank_redis_port', ''),
                    'bank_server_path': configs.get('bank_server_path', ''),
                    'bank_server_port': configs.get('bank_server_port', ''),
                    'bank_client_path': configs.get('bank_client_path', ''),
                    'bank_client_port': configs.get('bank_client_port', ''),
                    'bank_log_path': configs.get('bank_log_path', ''),
                    'bank_war_path': configs.get('bank_war_path', '')
                }
            }
        }
    }

    previous_data = read_yaml(yml_path)
    if previous_data is not None:
        for key in if_ele['data']:
            if not isinstance(if_ele['data'].get(key), list):
                if if_ele['data'].get(key) != previous_data['data'].get(key):
                    previous_data['data'][key] = if_ele['data'].get(key)
        clear_yaml(yml_path)
        write_yaml(yml_path, previous_data)
    else:
        write_yaml(yml_path, if_ele)
