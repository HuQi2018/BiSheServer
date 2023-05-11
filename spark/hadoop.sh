#! /bin/bash

# 该环境为centos7安装hadoop2.7的一键安装脚本（单机版）
# 使用时请注意修改15、16行的获取本机IP地址，以及修改24、25行的安装包文件存放的地址
# 脚本运行过程中有几个步骤需要自己手动输入yes，完成免密登陆（会有提示）
# 待安装完成会自动重启，重启后请直接运行命令“start-all.sh”启动hadoop，“start-spark-all.sh”启动spark

#7.0之后的版本
systemctl stop firewalld
systemctl disable firewalld

#7.0之前的版本
service iptables stop
chkconfig iptables off

#获取本机IP地址
echo "127.0.0.1 master" >> /etc/hosts

#配置主机名
echo "HOSTNAME=master" >> /etc/sysconfig/network

mkdir /root/hadoop

tar -xzvf ./jdk-8u65-linux-x64.tar.gz -C /root/hadoop/
tar -xzvf ./hadoop-2.7.1_64bit.tar.gz -C /root/hadoop/

mv /root/hadoop/hadoop-2.7.1 /root/hadoop/hadoop
mv /root/hadoop/jdk1.8.0_65 /root/hadoop/jdk

(ssh-keygen -t rsa;cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys;chmod 644 authorized_keys;sudo service sshd restart)

echo "" >> /etc/profile
echo "export JAVA_HOME=/root/hadoop/jdk" >> /etc/profile
echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> /etc/profile
echo "export HADOOP_HOME=/root/hadoop/hadoop" >> /etc/profile
echo "export HADOOP_MAPRED_HOME=\$HADOOP_HOME" >> /etc/profile
echo "export HADOOP_COMMON_HOME=\$HADOOP_HOME" >> /etc/profile
echo "export HADOOP_HDFS_HOME=\$HADOOP_HOME" >> /etc/profile
echo "export YARN_HOME=\$HADOOP_HOME" >> /etc/profile
echo "export HADOOP_COMMON_LIB_NATIVE_DIR=\$HADOOP_HOME/lib/native" >> /etc/profile
echo "export PATH=\$PATH:\$HADOOP_HOME/sbin:\$HADOOP_HOME/bin" >> /etc/profile
echo "export HADOOP_INSTALL=\$HADOOP_HOME" >> /etc/profile
echo "export HADOOP_OPTS=\"-Djava.library.path=\$HADOOP_HOME/lib:\$HADOOP_COMMON_LIB_NATIVE_DIR\"" >> /etc/profile
echo "" >> /etc/profile
source /etc/profile

sed -i "s/\${JAVA_HOME}/\/root\/hadoop\/jdk/g" /root/hadoop/hadoop/etc/hadoop/hadoop-env.sh

sed -i "s/<\/configuration>/ /g" /root/hadoop/hadoop/etc/hadoop/core-site.xml

echo -e "<property><name>hadoop.tmp.dir</name><value>/root/hadoop/hadoop/tmp</value></property>\n<property><name>fs.defaultFS</name><value>hdfs://master:9000</value></property>\n</configuration>" >> /root/hadoop/hadoop/etc/hadoop/core-site.xml

sed -i "s/<\/configuration>/ /g" /root/hadoop/hadoop/etc/hadoop/hdfs-site.xml

echo -e "<property><name>dfs.replication</name><value>1</value></property>\n</configuration>" >> /root/hadoop/hadoop/etc/hadoop/hdfs-site.xml

cp /root/hadoop/hadoop/etc/hadoop/mapred-site.xml.template /root/hadoop/hadoop/etc/hadoop/mapred-site.xml
sed -i "s/<\/configuration>/ /g" /root/hadoop/hadoop/etc/hadoop/mapred-site.xml

echo -e "<property><name>mapreduce.framework.name</name><value>yarn</value></property>\n</configuration>" >> /root/hadoop/hadoop/etc/hadoop/mapred-site.xml


sed -i "s/<\/configuration>/ /g" /root/hadoop/hadoop/etc/hadoop/yarn-site.xml

echo -e "<property><name>yarn.resourcemanager.hostname</name><value>Master</value></property>\n<property><name>yarn.nodemanager.aux-services</name><value>mapreduce_shuffle</value></property>\n</configuration>" >> /root/hadoop/hadoop/etc/hadoop/yarn-site.xml

echo "master" > /root/hadoop/hadoop/etc/hadoop/slaves

sh /root/hadoop/hadoop/bin/hdfs namenode -format




tar -xzvf ./spark-2.4.1-bin-hadoop2.7.tgz -C /root/hadoop/
tar -xzvf ./scala-2.10.4.tgz -C /root/hadoop/

mv /root/hadoop/scala-2.10.4 /root/hadoop/scala
mv /root/hadoop/spark-2.4.1-bin-hadoop2.7 /root/hadoop/spark

echo "" >> /etc/profile
echo "export SCALA_HOME=/root/hadoop/scala" >> /etc/profile
echo "export SPARK_HOME=/root/hadoop/spark" >> /etc/profile
echo "export PATH=\$PATH:\$SCALA_HOME/bin:\$SPARK_HOME/bin:\$SPARK_HOME/sbin" >> /etc/profile
echo "" >> /etc/profile
source /etc/profile

cp /root/hadoop/spark/conf/spark-env.sh.template /root/hadoop/spark/conf/spark-env.sh
echo "export JAVA_HOME=/root/hadoop/jdk" >> /root/hadoop/spark/conf/spark-env.sh
echo "export SCALA_HOME=/root/hadoop/scala" >> /root/hadoop/spark/conf/spark-env.sh
echo "export SPARK_MASTER_IP=master" >> /root/hadoop/spark/conf/spark-env.sh
echo "export MASTER=spark://master:7077" >> /root/hadoop/spark/conf/spark-env.sh
echo "export SPARK_WORKER_MEMORY=2048M" >> /root/hadoop/spark/conf/spark-env.sh
echo "export HADOOP_INSTALL=/root/hadoop/hadoop" >> /root/hadoop/spark/conf/spark-env.sh
echo "export HADOOP_CONF_DIR=\$HADOOP_INSTALL/etc/hadoop" >> /root/hadoop/spark/conf/spark-env.sh
echo "export LD_LIBRARY_PATH=/root/hadoop/hadoop/lib/native" >> /root/hadoop/spark/conf/spark-env.sh

cp /root/hadoop/spark/conf/slaves.template /root/hadoop/spark/conf/slaves
#echo "" >> /root/hadoop/spark/conf/slaves
#echo "Master" >> /root/hadoop/spark/conf/slaves

mv /root/hadoop/spark/sbin/start-all.sh /root/hadoop/spark/sbin/start-spark-all.sh
mv /root/hadoop/spark/sbin/stop-all.sh /root/hadoop/spark/sbin/stop-spark-all.sh

#ssh localhost

reboot

#sh start-all.sh

#hadoop fs -ls -R /

#sh stop-all.sh

#zkServer.sh start

#start-hbase.sh
