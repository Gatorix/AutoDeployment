import os
import subprocess
import traceback
import wmi
import signal


def kill_process(port):
    try:
        pid = os.popen('netstat -ano | findstr %s' % port).read().split('\n')[0].split(' ')[-1]
        if pid:
            os.kill(int(pid), signal.SIGILL)
            return '已终止端口为%s的进程！' % port
        else:
            return '%s端口未占用，无需终止！' % port
    except PermissionError:
        pid = os.popen('netstat -ano | findstr %s' % port).read().split('\n')[0].split(' ')[-1]
        if pid:
            run_as_admin('taskkill /F /PID %s' % pid)
            return '已终止端口为%s的进程！' % port
        else:
            return '%s端口未占用，无需终止！' % port
    except OSError as oe:
        return oe


def check_service(server_name):
    console = os.popen('sc query %s' % server_name)
    array = console.read().split(':')
    if len(array) != 3:
        state = array[3].split(' ')[3]
        if 'RUNNING' == state:
            return True, '获取服务状态：%s' % state
        else:
            return False, '获取服务状态：%s' % state
    else:
        return False, '服务未安装！'


def get_all_server():
    wmi_obj = wmi.WMI()
    services = wmi_obj.Win32_Service()
    for i in services:
        print("%d:%s -> %s [%s]" % (services.index(i) + 1, i.Name, i.Caption, i.State))


def cmd(command):
    sub = subprocess.Popen(command, stdout=subprocess.PIPE, encoding='gbk', stderr=subprocess.PIPE, shell=True)
    if sub.poll() == 0:
        return sub.communicate()
    else:
        return '命令： %s 执行完成 \n%s' % (command, sub.communicate()[1].replace('\n', ''))


def run_as_admin(command, timeout=1800000):
    f = None
    try:
        bat = r'.\shell\run_admin.bat'
        f = open(bat, 'w')
        f.write(command)
    except Exception as e:
        traceback.print_exc()
        raise e
    finally:
        if f:
            f.close()

    try:
        shell = r'.\shell\run_admin.vbs'
        sp = subprocess.Popen(
            shell,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        sp.wait(timeout=timeout)

        stderr = str(sp.stderr.read().decode("gbk")).strip()
        stdout = str(sp.stdout.read().decode("gbk")).strip()

        if "" != stderr:
            raise Exception(stderr)
        elif stdout.find("失败") > -1:
            raise Exception(stdout)
        else:
            return 1
    except Exception as e:
        raise e
