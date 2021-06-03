import pandas as pd
from pyspark import Row, SparkContext
from pyspark.sql import SQLContext, SparkSession


class Calculator():
    def __init__(self):
        # spark 初始化
        self.sql_spark = SparkSession. \
            Builder(). \
            appName('sql'). \
            master('local'). \
            getOrCreate()
        # mysql 配置
        self.prop = {'user': 'sql_bs_sju_site',
                'password': 'xzDPV7JL79w3Epg',
                'driver': 'com.mysql.cj.jdbc.Driver'}
        self.url = 'jdbc:mysql://127.0.0.1:3306/sql_bs_sju_site'

    def __del__(self):
        # 关闭spark会话
        self.sql_spark.stop()
        del self.sql_spark

    def show(self):
        # 读取表
        data = self.sql_spark.read.jdbc(url=self.url, table='(select user_id,tag_type,tag_weight,tag_name from user_usertag) aaa', properties=self.prop)
        # data.
        # 打印data数据类型
        print(type(data))
        # 展示数据
        data.show()


if __name__ == '__main__':

    Calculator().show()


def writ():
    # spark 初始化
    sc = SparkContext(master='local', appName='sql')
    spark = SQLContext(sc)
    # mysql 配置(需要修改)
    prop = {'user': 'sql_bs_sju_site',
            'password': 'xzDPV7JL79w3Epg',
            'driver': 'com.mysql.cj.jdbc.Driver'}
    url = 'jdbc:mysql://127.0.0.1:3306/sql_bs_sju_site'

    # 创建spark DataFrame
    # 方式1：list转spark DataFrame
    l = [(1, 12), (2, 22)]
    # 创建并指定列名
    list_df = spark.createDataFrame(l, schema=['id', 'value'])

    # 方式2：rdd转spark DataFrame
    rdd = sc.parallelize(l)  # rdd
    col_names = Row('id', 'value')  # 列名
    tmp = rdd.map(lambda x: col_names(*x))  # 设置列名
    rdd_df = spark.createDataFrame(tmp)

    # 方式3：pandas dataFrame 转spark DataFrame
    df = pd.DataFrame({'id': [1, 2], 'value': [12, 22]})
    pd_df = spark.createDataFrame(df)

    # 写入数据库
    pd_df.write.jdbc(url=url, table='new', mode='append', properties=prop)
    # 关闭spark会话
    sc.stop()

    # 创建DataFrame
    ## read.json
    # df = spark.read.json("examples/src/main/resources/people.json")
    # df = spark.read.load("examples/src/main/resources/people.json", format="json")  # format: Default to ‘parquet’
    # ## read.csv
    # df_csv = spark.read.csv("examples/src/main/resources/people.csv", sep=';', header=True)
    # ## read.text
    # df_txt = spark.read.text("examples/src/main/resources/people.txt")
    # ## read.parquet
    # df_parquet = spark.read.parquet("examples/src/main/resources/users.parquet")
    # ## orc
    # df_orc = spark.read.orc("examples/src/main/resources/users.orc")
    # ## rdd
    # sc = spark.sparkContext
    # rdd = sc.textFile('examples/src/main/resources/people.json')
    # df_rdd1 = spark.read.json(rdd)

    # createDataFrame: rdd, list, pandas.DataFrame
    # df_list = spark.createDataFrame([('Tom', 80), ('Alice', None)], ["name", "height"])
    # l = [('Alice', 1)]
    # rdd = sc.parallelize(l)
    # df_rdd2 = spark.createDataFrame(rdd, ['name', 'age'])
    # df_rdd2.show()
    # +-----+---+
    # | name | age |
    # +-----+---+
    # | Alice | 1 |
    # +-----+---+
    # ## with scheme
    # from pyspark.sql.types import *
    # schema = StructType([
    #     StructField("name", StringType(), True),
    #     StructField("age", IntegerType(), True)])
    # df3 = spark.createDataFrame(rdd, schema)
    # # from pandas
    # import pandas
    # df_pandas = spark.createDataFrame(pandas.DataFrame([[1, 2]]))
    # df_pandas.show()
    # +---+---+
    # | 0 | 1 |
    # +---+---+
    # | 1 | 2 |
    # +---+---+

    # 创建DataFrame, customers, products, sales
    # customers = [(1, 'James', 21, 'M'), (2, "Liz", 25, "F"), (3, "John", 31, "M"), \
    #              (4, "Jennifer", 45, "F"), (5, "Robert", 41, "M"), (6, "Sandra", 45, "F")]
    # df_customers = spark.createDataFrame(customers, ["cID", "name", "age", "gender"])  # list -> DF
    # products = [(1, "iPhone", 600, 400), (2, "Galaxy", 500, 400), (3, "iPad", 400, 300), \
    #             (4, "Kindel", 200, 100), (5, "MacBook", 1200, 900), (6, "Dell", 500, 400)]
    # df_products = sc.parallelize(products).toDF(["pId", "name", "price", "cost"])  # List-> RDD ->DF
    # sales = [("01/01/2015", "iPhone", "USA", 40000), ("01/02/2015", "iPhone", "USA", 30000), \
    #          ("01/02/2015", "iPhone", "China", 10000), ("01/02/2015", "iPhone", "China", 5000), \
    #          ("01/01/2015", "S6", "USA", 20000), ("01/02/2015", "S6", "USA", 10000), \
    #          ("01/01/2015", "S6", "China", 9000), ("01/02/2015", "S6", "China", 6000)]
    # df_sales = spark.createDataFrame(sales, ["date", "product", "country", "revenue"])

    # 基本操作
    # df_customers.cache()  # 以列式存储在内存中
    # df_customers.persist()  # 缓存到内存中
    # df_customers.unpersist()  # 移除所有的blocks
    # df_customers.coalesce(numPartitions=1)  # 返回一个有着numPartition的DataFrame
    # df_customers.repartition(10)  ##repartitonByRange
    # df_customers.rdd.getNumPartitions()  # 查看partitons个数
    # df_customers.columns  # 查看列名
    # ['cID', 'name', 'age', 'gender']
    # df_customers.dtypes  # 返回列的数据类型
    # df_customers.explain()  # 返回物理计划，调试时应用

    # 执行操作actions
    # df_customers.show(n=2, truncate=True, vertical=False)  # n是行数，truncate字符限制长度。
    # df_customers.collect()  # 返回所有记录的列表， 每一个元素是Row对象
    # df_customers.count()  # 有多少行,
    # df_customers.head(n=1)  # df_customers.limit(), 返回前多少行； 当结果比较小的时候使用
    # df_customers.describe()  # 探索性数据分析
    # df_customers.first()  # 返回第一行
    # df_customers.take(2)  # 以Row对象的形式返回DataFrame的前几行
    # df_customers.printSchema()  # 以树的格式输出到控制台
    # root
    # | -- cID: long(nullable=true)
    # | -- name: string(nullable=true)
    # | -- age: long(nullable=true)
    # | -- gender: string(nullable=true)
    # df_customers.corr('cID', "age")  # df_customers.cov('cID', 'age') 计算两列的相关系数

    # 转换：查询常用方法，合并，抽样，聚合，分组聚合，子集选取
    # 返回一个有新名的DataFrame
    # df_as1 = df_customers.alias("df_as1")

    # 聚合操作.agg: 一列或多列上执行指定的聚合操作，返回一个新的DataFrame
    # from pyspark.sql import functions as F
    # df_agg = df_products.agg(F.max(df_products.price), F.min(df_products.price), F.count(df_products.name))

    # 访问列
    # df_customers['age'] # 访问一列， 返回Column对象
    # df_customers[['age', 'gender']].show()
    # df_customers.cov('cID', 'age') 计算两列的相关系数

    # 去重，删除列
    # df_withoutdup = df_customers.distinct()  #distinct 去除重复行，返回一个新的DataFram， 包含不重复的行
    # df_drop = df_customers.drop('age', 'gender') # drop： 丢弃指定的列，返回一个新的DataFrame
    # df_dropDup = df_sales.dropDuplicates(['product', 'country'])  # dropDuplicates: 根据指定列删除相同的行
    # filter 筛选元素, 过滤DataFrame的行, 输入参数是一个SQL语句， 返回一个新的DataFrame

    # 行筛选和列选择
    # df_filter = df_customers.filter(df_customers.age > 25)
    # select 返回指定列的数据，返回一个DataFrame
    # df_select = df_customers.select('name','age')  # |    name|age|
    # df_select1 = df_customers.select(df_customers['name'], df_customers['age'] + 1)  # |    name|(age + 1)|
    # df_select2 = df_customers.selectExpr('name', 'age +1 AS new_age')  # |    name|new_age| 可以接收SQL表达式

    # 增加列，替换列
    ## withColumn 对源DataFrame 做新增一列或替换一原有列的操作， 返回DataFrame
    # df_new = df_products.withColumn("profit", df_products.price - df_products.cost)
    ## withColumnRenamed (existing, new)
    # df_customers.withColumnRenamed('age', 'age2')

    # 分组groupby
    # groupby/groupBy 根据参数的列对源DataFrame中的行进行分组
    # groupByGender = df_customers.groupBy('gender').count()
    # revenueByproduct = df_sales.groupBy('product').sum('revenue')

    # 替换replace
    # df_replace = df_customers.replace(["James", "Liz"], ["James2", "Liz2"], subset=["name"])

    # 缺失值处理(参数pandas.DataFrame类似)
    # from pyspark.sql import Row
    # df = sc.parallelize([ \
    #     Row(name='Alice', age=5, height=80), \
    #     Row(name=None, age=5, height=70), \
    #     Row(name='Bob', age=None, height=80)]).toDF()

    # dropna #na.drop删除包含缺失值的列，
    # df.na.drop(how='any', thresh=None, subset=None).show()  # df.dropna().show()
    # fillna # na.fill #
    # df.na.fill({'age': 5, 'name': 'unknown'}).show()

    # 遍历循环
    # ##foreach: 对DataFrame的每一行进行操作
    # def f(customer):
    #     print(customer.age)
    # df_customers.foreach(f)
    # ##foreachPartition, 对每一个Partition进行遍历操作

    # 合并
    # ## intersect 取交集，返回一个新的DataFrame
    # customers2 = [(11, 'Jackson', 21, 'M'), (12, "Emma", 25, "F"), (13, "Olivia", 31, "M"), \
    #               (4, "Jennifer", 45, "F"), (5, "Robert", 41, "M"), (6, "Sandra", 45, "F")]
    # df_customers2 = spark.createDataFrame(customers2, ["cID", "name", "age", "gender"])  # list -> DF
    # df_common = df_customers.intersect(df_customers2)
    ## union: 返回一个新的DataFrame, 合并行.
    # 一般后面接着distinct()
    # df_union = df_customers.union(df_customers2)  # 根据位置合并
    # df_union_nodup = df_union.distinct()
    # unionByName 根据列名进行行合并
    # df1 = spark.createDataFrame([[1, 2, 3]], ["col0", "col1", "col2"])
    # df2 = spark.createDataFrame([[4, 5, 6]], ["col1", "col2", "col0"])
    # df_unionbyname = df1.unionByName(df2)
    ## join： 与另一个DataFrame 上面执行SQL中的连接操作。 参数：DataFrame, 连接表达式，连接类型
    # transactions = [(1, 5, 3, "01/01/2015", "San Francisco"), (2, 6, 1, "01/02/2015", "San Jose"), \
    #                 (3, 1, 6, "01/01/2015", "Boston"), (4, 200, 400, "01/02/2015", "Palo Alto"), \
    #                 (6, 100, 100, "01/02/2015", "Mountain View")]
    # df_transactions = spark.createDataFrame(transactions, ['tId', "custId", "date", "city"])
    # df_join_inner = df_transactions.join(df_customers, df_transactions.custId == df_customers.cID, "inner")
    # df_join_outer = df_transactions.join(df_customers, df_transactions.custId == df_customers.cID, "outer")
    # df_join_left = df_transactions.join(df_customers, df_transactions.custId == df_customers.cID, "left_outer")
    # df_join_right = df_transactions.join(df_customers, df_transactions.custId == df_customers.cID, "right_outer")
    ##left_semi 返回在两个表都有的行，只返回左表
    ##left_anti 返回只在左表有的行

    # 排序
    # ## orderBy/sort 返回按照指定列排序的DataFrame. 默认情况下按升序(asc)排列
    # df_sort1 = df_customers.orderBy("name")
    # df_sort2 = df_customers.orderBy(['age', 'name'], ascending=[0, 1])
    # df_sort3 = df_customers.sort("name")
    # df_sort4 = df_customers.sort("name", ascending=False)

    # 抽样与分割
    # ## sample, 返回一个DataFrame, 包含源DataFrame 指定比例行数的数据
    # df_sample = df_customers.sample(withReplacement=False, fraction=0.2, seed=1)
    ## sampleBy 按指定列，分层无放回抽样
    # df_sample2 = df_sales.sampleBy('product', fractions={"iPhone": 0.5, "S6": 0.5}, seed=1)
    ## randomSplit: 把DataFrame分割成多个DataFrame
    # df_splits = df_customers.randomSplit([0.6, 0.2, 0.2])

    # 转化成其他常用数据对象， Json, DF, pandas.DF
    # df_json = df_customers.toJSON()  ## 返回RDD, RDD每个元素是JSON对象
    # df_json.first()
    # '{"cID":1,"name":"James","age":21,"gender":"M"}'
    # df_pandas = df_customers.toPandas()  ## 返回pandas.DataFrame
    # rdd = df_customers.rdd  # 然后可以使用RDD的操作
    # df = rdd.toDF().first()

    # 生成临时查询表
    # # registerTempTable. 给定名字的临时表, 用SQL进行查询
    # df_customers.registerTempTable("customers_temp")
    # df_search = spark.sql('select * from customers_temp where age > 30')
    # createGlobalTempView
    # createOrReplaceGlobalTempView  创建一个临时永久表，与Spark应该绑定
    # createOrReplaceTempView  生命周期与SparkSession绑定
    # createTempView

    # 其他函数
    # crossJion, crosstab, cube, rollup
    # 输出write，保存DataFrame到文件中
    # ## json, parquet, orc, csv,text 格式, 可以写入本地文件系统， HDFS, S3上
    # import os
    # df_customers0 = df_customers.coalesce(numPartitions=1)  # 设置NumPartition为1
    # # df_customers0.write.format('json').save("savepath")
    # # df_customers0.write.orc("savepath")
    # df_customers0.write.csv("savepath", header=True, sep=",", mode='overwrite')
    # # mode： 默认error/ append(追加)/ overwrite(重写)/ ignore(不写)
    # # df_customers0.write.parquet("savepath")