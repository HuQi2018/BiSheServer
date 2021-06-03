import ast
import json
import os
import re
import socket
import threading
import time

import requests
from botocore.exceptions import ConnectTimeoutError
from bs4 import BeautifulSoup
import sys
import pymysql
from requests import ConnectTimeout
from snownlp import SnowNLP
import configparser
import pyhdfs
from phone import Phone
import redis
# from BiSheServer.settings import CONFIG

sys.path.append("..")
# Create your tests here.
# from threading import Timer, ThreadError, current_thread, active_count

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_CONF_DIR = os.path.join(BASE_DIR, "config\conf.ini")
CONFIG = configparser.ConfigParser()
CONFIG.read(TEST_CONF_DIR, encoding='utf-8')
default = CONFIG.defaults()

# try:
#     socket.create_connection(("172.17.183.81", 50070))
# except Exception as ex:
#     print("Redis服务连接失败，日志上传模块恢复正常使用！")
POOL = redis.ConnectionPool(host=CONFIG.get('REDIS', 'REDIS_HOST'), port=8086,
                            password=CONFIG.get('REDIS', 'REDIS_PASSWORD'), max_connections=1000)
cache = redis.Redis(connection_pool=POOL)

HOST = "172.17.183.81"  # 地址
ROOT_PATH = "/test_data_log"  # 客户端连接的目录
REMOTE_PATH = "/test_data_log"  # HDFS上的路径，注意，需要先在hdfs手动创建此目录
LOCAL_PATH = "D:/tmp/output"  # 本地路径，建议写绝对路径，例如：E:\my_work\测试目录


class FileManager(object):

    # upload file to hdfs from local file system
    def file_upload(self, host, user_name, local_path, hdfs_path):
        print("file upload start")
        fs = pyhdfs.HdfsClient(hosts=host, user_name=user_name)
        print(fs.listdir('/'))
        fs.copy_from_local(local_path, hdfs_path)
        print("file upload finish")

    # download file from hdfs file system
    def file_down(self, host, user_name, local_path, hdfs_path):
        print("file download start")
        fs = pyhdfs.HdfsClient(hosts=host, user_name=user_name)
        fs.copy_to_local(hdfs_path, local_path)
        print("file download finish")


class Transfer(object):

    def __init__(self):
        self.host = HOST
        self.remotepath = REMOTE_PATH
        self.localpath = LOCAL_PATH
        self.rootpath = ROOT_PATH

        try:
            socket.create_connection(("172.17.183.81", 50070))
            self.client = pyhdfs.HdfsClient(self.host, user_name="root")
        except Exception as ex:
            self.client = ""

    def upload_file_windows(self):
        if not self.client:
            try:
                socket.create_connection(("172.17.183.81", 50070))
                self.client = pyhdfs.HdfsClient(self.host, user_name="root")
                print("Hadoop服务连接成功，日志上传模块恢复正常使用！")
            except Exception as ex:
                print("Hadoop连接失败,请检查Hadoop服务连接是否正常，日志上传模块恢复正常使用！", ex)
                return

        """windowsserver"""
        try:
            for root, dirs, files in os.walk(self.localpath):
                for file in files:
                    new_path = root.replace('\\', '/').replace(self.localpath, '')
                    upload_path = self.rootpath + new_path + '/' + file  # 上传的路径文件
                    local_path = self.localpath + new_path + '/' + file
                    print(upload_path)
                    print(local_path)
                    if not self.client.exists(upload_path):
                        self.client.copy_from_local(local_path, upload_path, overwrite=False)
        except Exception as e:
            print(e)


def get():
    url = 'https://movie.douban.com/subject/' + str(34434000) + '/'
    # https://movie.douban.com/j/subject_abstract?subject_id=34603816
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        html = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        return {"status": 0, "message": "获取失败！' + str(e) + '", "data": {}}
        # break
    if html.status_code == 404:
        return {"status": 0, "message": "获取失败，不存在有关信息！", "data": {}}
    data = {}
    soup = BeautifulSoup(html.text.encode("utf-8"), features='html.parser')
    soup = soup.find(name='div', attrs={'id': 'wrapper'})
    print(soup.h1.span.string)
    data['type'] = type  # 类型
    data['title'] = soup.h1.span.string  # 标题
    article = soup.find(name='div', attrs={'class': 'subjectwrap'})
    data['article'] = str(article)  # 信息
    sum = soup.find(name='div', attrs={'id': 'link-report'})
    summary = sum.find(name='span', attrs={'class': 'short'})
    if summary:
        summary = str(summary)
    else:
        summary = str(sum)
    data['summary'] = str(summary)  # 简述内容简介
    allSummary = soup.find(name='span', attrs={'class': 'all hidden'})
    data['allSummary'] = str(allSummary)  # 内容简介
    if type == 'book':
        intro = soup.find(text='作者简介')
        if intro:
            try:
                data['info'] = str(intro.parent.parent.next_sibling.next_sibling.div.div.text)  # 作者简介
            except:
                data['info'] = str(intro.parent.parent.next_sibling.next_sibling.span.div.text)  # 作者简介
                pass
        # print(data['info'])
        tag = soup.find(name='div', attrs={'id': 'db-tags-section'})
        tags = [td.a.string for td in tag.div.find_all('span')]
    else:
        tag = soup.find(name='div', attrs={'class': 'tags-body'})
        tags = [td.string for td in tag.find_all('a')]
    data['tags'] = tags  # 标签
    print(data)
    # data = json.dumps(data)
    return {"status": 1, "message": "获取成功！", "data": str(data), "url": str(url)}


def emoution(sentece):
    sent = SnowNLP(sentece)
    predict = sent.sentiments
    return predict*100


def detabase():
    db = pymysql.connect("localhost", "sql_bs_sju_site", "xzDPV7JL79w3Epg", "sql_bs_sju_site")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "SELECT `movie_id`,`rating` FROM `sql_bs_sju_site`.`movie_collectmoviedb`"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            # print(row)
            movie_id = row[0]
            rating = row[1]
            # 打印结果
            ratingData = json.loads(rating.replace("'",'"'))
            average = ratingData['average']
            if average != 0:
                sql2 = "INSERT INTO `sql_bs_sju_site`.`movie_movieratingdb`(movie_id_id, rating) VALUES ('{}', '{}')".format(movie_id, average)
                try:
                    print(sql2)
                    # 执行sql语句
                    cursor.execute(sql2)
                    # 提交到数据库执行
                    db.commit()
                except Exception as ex:
                    print("插入失败！{}".format(ex))
                    # 如果发生错误则回滚
                    db.rollback()
            print("电影ID：{}  电影评分：{}".format(movie_id,average))
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()


def pubdatebase():
    db = pymysql.connect("localhost", "sql_bs_sju_site", "xzDPV7JL79w3Epg", "sql_bs_sju_site")
    # 使用 cursor() 方法创建一个游标对象 cursor
    date_match = re.compile(r'^[\d]{4}-[\d]{2}-[\d]{2}$')
    cursor = db.cursor()
    sql = "SELECT pubdate,mainland_pubdate,pubdates,movie_id FROM sql_bs_sju_site.movie_collectmoviedb"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            # print(row)
            pubdate = row[0]
            mainland_pubdate = row[1]
            pubdates = row[2]
            movie_id = row[3]
            date = ""
            if pubdate and date_match.match(pubdate):
                date = pubdate
            elif mainland_pubdate and date_match.match(mainland_pubdate):
                date = mainland_pubdate
            elif pubdates != "[]":
                pubdate = ast.literal_eval(pubdates)
                pubdate = pubdate[-1]
                pubdate = pubdate[:pubdate.find('(')]
                if len(pubdate) == 7:
                    pubdate = pubdate + "-01"
                elif len(pubdate) == 4:
                    pubdate = pubdate + "-01-01"
                elif len(pubdate) == 9:
                    pubdate = pubdate[:-1] + "0" + pubdate[-1:]
                if date_match.match(pubdate):
                    date = pubdate
            else:
                continue
            print(date)
            if date:
                sql2 = "INSERT INTO `sql_bs_sju_site`.`movie_moviepubdatedb` (movie_id_id, pubdate) VALUES ('{}', '{}')"\
                    .format(movie_id, date)
                try:
                    # print(sql2)
                    # 执行sql语句
                    cursor.execute(sql2)
                    # 提交到数据库执行
                    db.commit()
                except Exception as ex:
                    print("插入失败！{}".format(ex))
                    # 如果发生错误则回滚
                    db.rollback()
            print("电影ID：{}  电影上映日期：{}".format(movie_id,date))
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()


def movie_tag_database():
    db = pymysql.connect("localhost", "sql_bs_sju_site", "xzDPV7JL79w3Epg", "sql_bs_sju_site")
    cursor = db.cursor()

    def insert(type,data):
        sql2 = "INSERT INTO `sql_bs_sju_site`.`movie_movietagdb` (movie_id_id, tag_type, tag_name) " \
               "VALUES ('{}', '{}', '{}')".format(
            movie_id, type, data)
        try:
            # print(sql2)
            # 执行sql语句
            cursor.execute(sql2)
            # 提交到数据库执行
            db.commit()
        except Exception as ex:
            print("插入失败！{}".format(ex))
            # 如果发生错误则回滚
            db.rollback()
        print("电影ID：{}  电影标签：{}  电影标签名：{}".format(movie_id, type, data))

    sql = "SELECT `tags`,`genres`,`countries`,`languages`,`year`,`movie_id` FROM sql_bs_sju_site.movie_collectmoviedb"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            tags = row[0]
            genres = row[1]
            countries = row[2]
            languages = row[3]
            year = row[4]
            movie_id = row[5]
            if tags:
                tags = ast.literal_eval(tags)
                for tag in tags:
                    insert("tag", tag)
            if genres:
                genres = ast.literal_eval(genres)
                for genre in genres:
                    insert("genre", genre)
            if countries:
                countries = ast.literal_eval(countries)
                for country in countries:
                    insert("country", country)
            if languages:
                languages = ast.literal_eval(languages)
                for language in languages:
                    insert("language", language)
            if year:
                insert("year", year)
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()


def testThreadPrint(key):
    print(key)


class TagThread(threading.Thread):
    def __init__(self, func, args):
        self.func = func
        self.kwargs = args
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(3)
        eval(str(self.func)+'("'+str(self.kwargs)+'")')


def sql_test():

    db = pymysql.connect("localhost", "sql_bs_sju_site", "xzDPV7JL79w3Epg", "sql_bs_sju_site")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select tag_name from user_usertag where tag_type='info_movie_type' and user_id=1 " \
          "ORDER BY tag_weight DESC LIMIT 0,5"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        li_tags = []
        for row in results:
            li_tags.append(row[0])
            print(row[0])
            # movie_id = row[0]
        count_tag = len(li_tags)
        if count_tag >= 4:
            sql2 = "select movie_id_id from movie_movietagdb where tag_name='" + li_tags[1] + "' and  tag_type='genre' and movie_id_id in (select movie_id_id from movie_movietagdb where tag_name='" + li_tags[0] + "' and tag_type='genre')"
            cursor.execute(sql2)
            results2 = cursor.fetchall()
            for row2 in results2:
                print(row2)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    # TagThread(func="testThreadPrint", args=[123, 123, 34]).start()
    # print(CONFIG.get('DATEBASE', 'DATABASES_ENGINE'))
    # print(emoution("好，非常好！"))
    # # print(emoution("坏，非常坏！"))
    # print(cache.get("test"))
    # print(detabase())
    # detabase()
    # pubdatebase()
    # movie_tag_database()

    sql_test()

    # transfer = Transfer()
    # transfer.upload_file_windows()

    # phoneNum = '13727065853'
    # info = Phone().find(phoneNum)
    # print(info)
    # try:
    #     phone = info['phone']
    #     province = info['province']
    #     city = info['city']
    #     zip_code = info['zip_code']
    #     area_code = info['area_code']
    #     phone_type = info['phone_type']
    # except:
    #     print('none')

