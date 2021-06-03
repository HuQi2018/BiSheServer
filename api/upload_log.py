import datetime
import socket
import threading

import pyhdfs
import os

from BiSheServer.settings import CONFIG, BASE_LOG_DIR, LOG_SUFFIX


# HOST = "172.17.183.81"  # 地址
# ROOT_PATH = "/test_data_log"  # 客户端连接的目录
# REMOTE_PATH = "/test_data_log"  # HDFS上的路径，注意，需要先在hdfs手动创建此目录
# LOCAL_PATH = "/www/myspark/log"  # 本地路径，建议写绝对路径，例如：E:\my_work\测试目录  "D:/tmp/output"


class LogThread(threading.Thread):
    def __init__(self, func, args):
        self.func = func
        self.kwargs = args
        threading.Thread.__init__(self)

    def run(self):
        eval(str(self.func)+'("'+str(self.kwargs)+'")')


class Transfer(object):

    def __init__(self):
        # 注意host的值在本地hosts文件中是否指向HADOOP_HOST地址，
        # 如HTTPConnectionPool(host='desktop-wonder.localdomain', port=50075)
        self.host = CONFIG.get('HADOOP_LOG', 'HADOOP_HOST')
        self.remotepath = CONFIG.get('HADOOP_LOG', 'REMOTE_PATH')
        self.localpath = CONFIG.get('HADOOP_LOG', 'LOCAL_PATH')
        self.rootpath = BASE_LOG_DIR
        try:
            socket.create_connection((self.host, 50070))
            self.client = pyhdfs.HdfsClient(self.host, user_name="root")
        except Exception as ex:
            self.client = ""
            print(ex)

    # 上传单个文件
    def upload_single_file(self, local_path, upload_path):
        if not self.client:
            try:
                socket.create_connection((self.host, 50070))
                self.client = pyhdfs.HdfsClient(self.host, user_name="root")
                print("Hadoop服务连接成功，日志上传模块恢复正常使用！")
            except Exception as ex:
                self.client = ""
                print("Hadoop连接失败,请检查Hadoop服务是否正常，日志上传模块无法使用！", ex)
                return
        try:
            upload_path = self.remotepath + "/" + upload_path
            if not self.client.exists(upload_path):
                self.client.copy_from_local(local_path, upload_path, overwrite=False)
            else:
                print("文件已存在！" + upload_path)
        except Exception as e:
            print(e)

    # 上传文件夹到hadoop，可遍历子文件夹
    def upload_file_windows(self):
        if not self.client:
            try:
                socket.create_connection((self.host, 50070))
                self.client = pyhdfs.HdfsClient(self.host, user_name="root")
                print("Hadoop服务连接成功，日志上传模块恢复正常使用！")
            except Exception as ex:
                self.client = ""
                print("Hadoop连接失败,请检查Hadoop服务是否正常，日志上传模块无法使用！", ex)
                return
        """windowsserver"""
        try:
            for root, dirs, files in os.walk(self.localpath):
                for file in files:
                    new_path = root.replace('\\', '/').replace(self.localpath, '')
                    upload_path = self.rootpath + new_path + '/' + file  # 上传的路径文件
                    local_path = self.localpath + new_path + '/' + file
                    if not self.client.exists(upload_path):
                        self.client.copy_from_local(local_path, upload_path, overwrite=False)

        except Exception as e:
            print(e)


# 线程启动上传
def upload_hadoop_log_thread(suffix):
    LogThread(func="upload_hadoop_log", args=suffix).start()


# 上传系统日志文件
def upload_hadoop_log(suffix):
    transfer = Transfer()
    print("执行定时上传日志任务！" + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    # upload_path = transfer.rootpath.replace('\\', '/')  # 上传的路径文件
    local_path = transfer.rootpath.replace('\\', '/')
    if suffix != "":
        suffix = "." + suffix + ".log"
    else:
        suffix = "." + (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime(LOG_SUFFIX) + ".log"
    transfer.upload_single_file(local_path + 'mysite_debug' + suffix, 'mysite_debug' + suffix)
    transfer.upload_single_file(local_path + 'mysite_api' + suffix, 'mysite_api' + suffix)
# if __name__ == '__main__':
#     transfer = Transfer()
#     transfer.upload_file_windows()
