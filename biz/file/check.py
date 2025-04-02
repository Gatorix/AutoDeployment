import os


def check_path(path, *keys):
    temp = []
    key_results = []
    for root, dirs, files in os.walk(path):
        temp.append(dirs)
    try:
        for key in keys:
            if key in temp[0]:
                key_results.append(True)
        if all([key_results]):
            return True
        else:
            return False
    except IndexError:
        return False

# print(check_path('D:\Tools\latest\latest', 'WEN-INF', 'stati2c', ))
