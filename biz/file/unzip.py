import zipfile
import os


def un_zip(zip_file_path, un_zip_path, is_direct_unzip=False, folder_name=''):
    try:
        zip_file = zipfile.ZipFile(zip_file_path)
        if is_direct_unzip:
            if os.path.isdir('%s/%s' % (un_zip_path, folder_name)):
                del zip_file
                return False, '解压失败：已存在同名文件夹，请删除后重试！'
            else:
                # count = 0
                for names in zip_file.namelist():
                    # count += 1
                    zip_file.extract(names, '%s/%s' % (un_zip_path, folder_name))
                    # print('unzip: %s --%s' % (names, '%s%%' % round(count / len(zip_file.namelist()) * 100, 2)))
                zip_file.close()
                del zip_file
                os.remove(zip_file_path)
                return True, '解压完成！'
        else:
            if os.path.isdir('%s/%s' % (un_zip_path, zip_file_path.split('\\')[-1][:-4])):
                del zip_file
                return False, '解压失败：已存在同名文件夹，请删除后重试！'
            else:
                # count = 0
                for names in zip_file.namelist():
                    # count += 1
                    zip_file.extract(names, "%s/%s" % (un_zip_path, zip_file_path.split('/')[-1][:-4]))
                    # print('unzip: %s --%s' % (names, '%s%%' % round(count / len(zip_file.namelist()) * 100, 2)))
                zip_file.close()
                del zip_file
                os.remove(zip_file_path)
                return True, '解压完成！'
    except PermissionError as pe:
        return False, '解压失败：权限错误%s' % pe

# print(un_zip(r'D:\Code\auto-deployment\data\temp\B20220500158.zip', r'D:\Code\test'))
# print(os.listdir(r'D:\Code\test'))
# if os.path.isdir(r'D:\Code\test\mysql-5.7.36-winx64.zip'):
#     print(111)
