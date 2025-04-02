import os
import socket
import requests
import webbrowser


def port_is_used(port, ip='127.0.0.1'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        return False, '本机端口%d已被占用，请尝试其他端口！' % int(port)
    except ConnectionRefusedError:
        return True, '本机端口%d未被占用！' % int(port)
    except (OverflowError, TypeError, ValueError):
        return False, '端口号输入错误，请输入0-65535之间的整数！'


def open_browser(url):
    webbrowser.open(url, new=0)


# http://192.168.0.50:8091/patch/system/extend.do?branch=t2-v3.4&method=getBuildPatchFile&buildPatchNo=BFS.T3.4.0000.2022051801
def get_structure(structure_name: str):
    url = "http://192.168.0.50:8090/patch/system/extend.do?" \
          "branch=t2-v3.4&method=getBuildPackFile&buildPackNo=%s" % structure_name

    if os.path.isdir('%s\\data\\temp' % os.getcwd()):
        pass
    else:
        os.mkdir('%s\\data\\temp' % os.getcwd())

    try:
        r = requests.get(url)
        if r.headers.get('Content-Disposition'):
            if '.zip' in structure_name:
                structure_name = structure_name.replace('.zip', '')
            with open("%s\\data\\temp\\%s.zip" % (os.getcwd(), structure_name), "wb") as zip_pack:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        zip_pack.write(chunk)
            return True, '%s下载成功！' % structure_name
        else:
            return False, r.content.decode('utf-8')
    except requests.exceptions.ConnectTimeout as rec:
        return False, '构建包获取失败！\n连接超时：%s' % rec
    except FileNotFoundError as ffe:
        return False, '构建包获取失败！\n%s' % ffe
# get_structure('B20220600040')

def get_structure_time(structure_name):
    url = "http://192.168.5.171:8080/WebContent/system/extend.do?" \
          "branch=t2-v3.4&method=getBuildPackFileTime&buildPackNo=%s" % structure_name
    try:
        r = requests.get(url)
        return True, r.content.decode('utf8')
    except requests.exceptions.ConnectTimeout as rec:
        return False, '构建时间获取失败！\n连接超时：%s' % rec
    except FileNotFoundError as ffe:
        return False, '构建时间获取失败！\n%s' % ffe


def get_patch(patch_name=''):
    url = "http://192.168.0.50:8090/patch/system/extend.do?branch=t2-v3.4&" \
          "branch=t2-v3.4&method=getBuildPatchFile&fileType=epatch&buildPatchNo=%s" % patch_name

    if os.path.isdir('.\\data\\temp'):
        pass
    else:
        os.mkdir('.\\data\\temp')

    try:
        r = requests.get(url)
        if r.headers.get('Content-Disposition'):

            if '.patch' in patch_name:
                patch_name = patch_name.replace('.patch', '')
            else:
                patch_name_from_header = r.headers.get('Content-Disposition').split('=')[-1]
                patch_name = '.'.join(patch_name_from_header.split('.')[:-1]) if patch_name == '' else patch_name

            with open("%s\\data\\temp\\%s.patch" % (os.getcwd(), patch_name), "wb") as patch:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        patch.write(chunk)

            return True, '%s加密补丁包下载成功！' % patch_name
        else:
            return False, r.content.decode('utf-8')
    except requests.exceptions.ConnectTimeout as rec:
        return False, '加密补丁包获取失败！\n连接超时：%s' % rec
    except FileNotFoundError as ffe:
        return False, '加密补丁包获取失败！\n%s' % ffe
