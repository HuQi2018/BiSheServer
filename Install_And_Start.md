# 系统安装和启动教程

## 一、前期数据和软件准备
```
从网盘中下载基础软件和基础数据：
    链接: https://pan.baidu.com/s/1XJTnuCVlDvbUG3zp4kk-Ag 提取码: ik32

分享目录结构说明：
├─centos                                  （安装Hadoop、Spark单机所用的Linux软件）
│  ├─spark.py                            （离线推荐计算python程序）
│  ├─hadoop.sh                           （Hadoop、Spark一键安装执行脚本）
│  ├─requirements.txt      	            （spark.py运行所需库）
│  ├─CentOS-7-x86_64-DVD-2009.iso      	（Centos安装镜像）
│  ├─scala-2.10.4.tgz      	            （Scala软件）
│  ├─jdk-8u65-linux-x64.tar.gz      	    （Jdk软件）
│  ├─spark-2.4.1-bin-hadoop2.7.tgz      	（Spark软件）
│  ├─mysql-connector-java-8.0.24.jar      （MySQL连接驱动jar包）
│  └─hadoop-2.7.1_64bit.tar.gz            （Hadoop软件）
│
├─soft                                                                          （需要在Windows中安装的软件）
│  ├─VMware-workstation-full-16.0.0 许可号：ZF3R0-FHED2-M80TY-8QYGC-NPKYF.exe   （虚拟机软件）
│  ├─mysql-installer-community-5.7.37.0.msi                                     （MySQL软件）
│  ├─python-3.8.2.exe                                                           （Python软件）
│  ├─Redis-x64-5.0.10.msi                                                       （Redis软件）
│  ├─WinSCP-5.19.4-Setup.exe                                                    （WinSCP连接Linux的软件，可用于传输文件到Linux）
│  └─putty.zip                                                                  （WinSCP配套连接控制台终端软件）
│
├─other_sql.sql                            （焦点图、地址信息等数据）
├─movie_collectmoviedb.sql                 （电影基础数据）
├─movie_movietagdb.sql                     （电影标签处理后的数据）
└─表结构.sql                               （不必要的导入表结构数据）

```

## 二、系统环境安装

### 1、MySQL、Redis、Python3基础环境安装

```
1、运行 mysql-installer-community-5.7.37.0.msi 安装MySQL；
    MySQL安装完成后自行建一个表，注意在创建数据库时请注意将数据库的字符编码设置为utf-8编码集，
    否则后面运行命令“python manage.py migrate”会报错。
2、运行 Redis-x64-5.0.10.msi 安装Redis；
3、运行 python-3.8.2.exe 安装Python3；
```

### 2、安装系统所需的库

```
在项目目录（最外层包含 requirements.txt）运行命令，安装系统运行所需库：
pip3 install --index https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt

等待安装完成，显示 Successfully 字样表示成功即可。
```

### 3、修改系统配置

```
当外部配置完成后，可将本系统根目录中config/conf.ini文件打开，然后修改其中的配置。
首先是系统的默认配置服务、MySql数据库配置、Redis数据库配置、邮件验证系统配置和Hadoop等配置。
MySql数据库配置、Redis数据库配置 必须根据自己上述 1 安装时所配置的参数进行配置。
邮件系统主要用于用户注册使用，若无邮件服务（该服务需自行更改为自己的配置，默认是无效的配置），可选择关闭，关闭后会直接在点击发送验证码的下方提示验证码，输入即可。
Hadoop配置主要用于系统运行时产生的日志进行上传到HDFS使用，非必要配置，可选择关闭。
```

### 4、创建表结构及导入基础数据

```
在项目目录运行命令，创建表结构，同时创建Django管理系统的管理员帐号：
    python manage.py makemigrations
    python manage.py makemigrations user movie api
    python manage.py migrate
    python manage.py createsuperuser                   # 创建 Django 后台登录账户

上述命令运行完后，导入基础数据：
    movie_collectmoviedb.sql  -》  movie_movietagdb.sql  -》  other_sql.sql
    根据以上顺序执行sql，无错误表示成功。
```

### 5、项目启动运行

    上述所有工作都准备完成后，在项目目录下使用命令启动该系统服务：
    python manage.py runserver 8001
    若无报错，则可访问 http://127.0.0.1:8001 浏览该系统，导入的默认账号为  Zero  123456  。

## 三、离线处理服务环境搭建

    非必要部分，此部分涉及系统的导航栏中的“猜你喜欢”模块的内容推荐部分，只用于离线处理部分，不安装也可运行整个系统
    主要使用Hadoop、Spark组件，运行脚本spark.py文件，执行离线计算，数据来源于MySQL中的用户操作、用户标签（用户画像）、电影数据输入，
    生成推荐内容到MySQL数据库 user_usermovierecommend 表中

### 1、安装虚拟机软件

```

├─centos                                  （安装Hadoop、Spark单机所用的Linux软件）
│  ├─spark.py                            （离线推荐计算python程序）
│  ├─hadoop.sh                           （Hadoop、Spark一键安装执行脚本）
│  ├─requirements.txt      	            （spark.py运行所需库）
│  ├─scala-2.10.4.tgz      	            （Scala软件）
│  ├─jdk-8u65-linux-x64.tar.gz      	    （Jdk软件）
│  ├─spark-2.4.1-bin-hadoop2.7.tgz      	（Spark软件）
│  ├─mysql-connector-java-8.0.24.jar      （MySQL连接驱动jar包）
│  └─hadoop-2.7.1_64bit.tar.gz            （Hadoop软件）

1、安装软件：VMware-workstation-full-16.0.0 许可号：ZF3R0-FHED2-M80TY-8QYGC-NPKYF.exe
2、软件安装完成后，使用 CentOS-7-x86_64-DVD-2009.iso 创建虚拟机；
3、安装 WinSCP-5.19.4-Setup.exe  使用该软件将上述文件传输到 Centos 中；
```

### 2、安装Hadoop、Spark软件环境

```
运行命令：
    bash hadoop.sh
    此脚本安装的为 hadoop2.7、spark2.4.1 单机版本，为方便，此处使用已写好的一键安装脚本进行安装。
    如需安装更高版本、伪分布式 或 熟悉安装过程，请自行百度进行了解。
    注意，脚本执行过程中，有几处会停留，需要手动按回车，执行完后会自动重启，
    重启后请直接运行命令“start-all.sh”启动hadoop，“start-spark-all.sh”启动spark。

验证安装：
    下方以“ip”表示安装Hadoop、Spark的虚拟机地址（具体可用 ifconfig 命令查看）
    1、访问Hadoop：http://ip:50070
    2、访问Spark：http://ip:8080
    3、执行命令：spark-shell
    若上述都正常，表示安装成功。

```

### 3、安装spark.py运行环境

```
运行命令，安装Python3：
    yum install -y python3
在上述 requirements.txt 文件目录下执行，安装spark.py运行环境：
    pip3 install --index https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
安装Spark连接MySQL的驱动：
    将文件 mysql-connector-java-8.0.24.jar 文件复制到spark的jars目录里即可。
```

### 4、修改 spark.py 文件中的配置

```
需要修改mysql数据库配置信息（33行、34行、36行）
数据库的IP请在windows中使用命令 “ipconfig” 获取，在linux校验查看是否能ping通该IP地址
```

### 5、执行离线推荐处理脚本 spark.py

```
运行命令，执行离线推荐处理脚本：
    python3 spark.py
    运行时间由机器性能和数据量决定，可通过 http://ip:8080 查看运行状况，同时HDFS中会生成处理过程文件。
    运行完后，可以再数据库 user_usermovierecommend 表中查看推荐数据，若推荐为空则表示该用户的操作数据太少，不足以生成推荐内容。

该命令可以加入到 Crontab 定时计划任务中，即可每日自动处理，生成推荐内容。
spark.py 中同时包含基于电影内容（基于内容）、基于用户相似度（基于协同过滤）推荐的方式默认只使用了基于协同过滤推荐。
后期如有兴趣的同学还可完善，同时进一步改为实时推荐。
```
