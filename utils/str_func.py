import re
import random
import string
import datetime


def get_current_date():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def convert_slash(path):
    if isinstance(path, str):
        return path.replace('\\', '/')


def check_url(url):
    p = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}' \
        r'([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):(6553[0-5]|655[0-2][0-9]|' \
        r'65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{1,3}|[0-9])$'

    # return all([bool(re.match(r'http[s]?:+', url.split('//')[0])),
    #             bool(re.match(p, url.split('//')[1]))]) if '//' in url else False
    return bool(re.match(p, url))


# print(check_url('127.0.0.1:3306'))
def random_str(lens=4):
    return ''.join(random.choice(string.ascii_letters) for _ in range(lens))


def check_structure_name(structure: str):
    if ',' in structure:
        result_list = []
        structure_list = structure.split(',')
        if structure_list:
            for _ in structure_list:
                result_list.append(check_structure_name(_))
        return result_list
    else:
        if structure.startswith('B') and len(structure) == 12:
            return True
        elif structure.startswith('V') and len(structure) == 9:
            return True
        elif structure.startswith('batch') and len(structure) == 19:
            return True
        else:
            return False


def check_patch_name(patch: str):
    if ',' in patch:
        return False
    else:
        if patch.startswith('BFS.') and len(patch.split('.')[4]) == 10:
            return True
        else:
            return False


# print(check_patch_name('BFS.T3.4.0000.2022052301.Beta.patch'))
# print(isinstance(check_structure_name('B20220500158'), list))

# print(check_structure_name('B20220500158,B20220500158'))
# te = ['B20220500158', 'B20220500158', 'B20220500158', 'B20220500158']
# test = [True, True, False, True]
# temp = []
# for _ in test:
#     if not _:
#         temp.append(test.index(_))
# print(temp)
# for _ in temp:
#     print(te[_])
