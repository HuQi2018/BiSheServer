import datetime
# import time

# from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api import model_json
from user.models import UsersBase


# 电影类型表
class CollectMovieTypeDB(models.Model):
    movie_type = models.CharField(max_length=100, unique=True, default='', verbose_name=u"电影类型")

    def __str__(self):
        return self.movie_type

    class Meta:
        verbose_name = '电影类型表'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# class MovieBase(models.Model):
#     movie_id = models.IntegerField(unique=True, null=False,verbose_name=u"电影ID")  # 唯一标识
#     original_title = models.CharField(max_length=1000, unique=True, null=False, default='',
#                                       verbose_name=u"原始标题")  # 原始标题
#     title = models.CharField(max_length=1000, unique=True, null=False, default='', verbose_name=u"中文标题")  # 中文标题
#     aka = models.CharField(max_length=1000, default='',verbose_name=u"又名")  # 又名
#     average_rating = models.IntegerField(default=0,verbose_name=u"平均评分")  # 评分数
#     ratings_count = models.IntegerField(default=0, verbose_name=u"评分数")  # 评分数
#     pubdate = models.DateField(unique=True, null=False, default='', verbose_name=u"上映日期")  # 上映日期
#     year = models.IntegerField(unique=True, null=False, default=0, verbose_name=u"年份")  # 年份
#     countries = models.CharField(max_length=1000, default='', verbose_name=u"制片国家/地区")  # 制片国家/地区
#     tags = models.CharField(max_length=1000, default='', verbose_name=u"标签")  # 标签
#     genres = models.CharField(max_length=1000, default='', verbose_name=u"类型")  # 类型
#     collect_count = models.IntegerField(default=0, verbose_name=u"收藏")  # 收藏
#     images = models.TextField(default='',verbose_name=u"封面图片")  # 封面图片
#     photos = models.TextField(default='',verbose_name=u"照片")  # 照片
#     languages = models.CharField(max_length=1000, default='',verbose_name=u"语言")  # 语言
#     actor = models.TextField(default='', verbose_name=u"演员")  # 演员
#     record_time = models.DateTimeField(auto_now_add=True,verbose_name=u"录入时间")

# 电影详情数据
class CollectMovieDB(models.Model):
    movie_id = models.IntegerField(unique=True, null=False, verbose_name=u"电影ID")  # 唯一标识
    original_title = models.CharField(max_length=1000, default='', verbose_name=u"原始标题")  # 原始标题
    title = models.CharField(max_length=1000, default='', verbose_name=u"中文标题")  # 中文标题
    rating = models.TextField(default='', verbose_name=u"评分")  # 评分
    ratings_count = models.IntegerField(default=0, verbose_name=u"评分数")  # 评分数
    pubdate = models.CharField(max_length=1000, default='', verbose_name=u"上映日期")  # 上映日期
    pubdates = models.CharField(max_length=1000, default='', verbose_name=u"上映日期2")  # 上映日期2
    year = models.IntegerField(default=0, verbose_name=u"年份")  # 年份
    countries = models.CharField(max_length=1000, default='', verbose_name=u"制片国家/地区")  # 制片国家/地区
    mainland_pubdate = models.CharField(max_length=1000, default='', verbose_name=u"主要上映日期")  # 主要上映日期
    aka = models.CharField(max_length=1000, default='', verbose_name=u"又名")  # 又名
    tags = models.CharField(max_length=1000, default='', verbose_name=u"标签")  # 标签
    durations = models.TextField(default='', verbose_name=u"时长")  # 时长
    genres = models.CharField(max_length=1000, default='', verbose_name=u"类型")  # 类型
    videos = models.TextField(default='', verbose_name=u"短视频")  # 短视频
    wish_count = models.IntegerField(default=0, verbose_name=u"想看")  # 想看
    reviews_count = models.IntegerField(default=0, verbose_name=u"短评数")  # 短评数
    comments_count = models.IntegerField(default=0, verbose_name=u"评论数")  # 评论数
    collect_count = models.IntegerField(default=0, verbose_name=u"收藏")  # 收藏
    images = models.TextField(default='', verbose_name=u"封面图片")  # 封面图片
    photos = models.TextField(default='', verbose_name=u"照片")  # 照片
    languages = models.CharField(max_length=1000, default='', verbose_name=u"语言")  # 语言
    writers = models.TextField(default='', verbose_name=u"作者")  # 作者
    actor = models.TextField(default='', verbose_name=u"演员")  # 演员
    summary = models.TextField(default='', verbose_name=u"简介")  # 简介
    directors = models.TextField(default='', verbose_name=u"导演")  # 导演
    record_time = models.DateTimeField(auto_now_add=True, verbose_name=u"录入时间")

    def __str__(self):
        # return str(self.movie_id)
        return '%s - %s' % (self.movie_id, self.title)

    class Meta:
        verbose_name = '电影详情数据'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 豆瓣前250电影
class CollectTop250MovieDB(models.Model):
    movie_id = models.IntegerField(unique=True, null=False, verbose_name=u"电影ID")
    movie_title = models.TextField(default='', verbose_name=u"中文标题")
    movie_original_title = models.TextField(default='', verbose_name=u"原始标题")
    movie_rating = models.TextField(default='', verbose_name=u"评分")
    movie_year = models.IntegerField(default=0, verbose_name=u"年份")
    movie_pubdates = models.TextField(default='', verbose_name=u"上映日期")
    movie_directors = models.TextField(default='', verbose_name=u"导演")
    movie_genres = models.TextField(default='', verbose_name=u"类型")
    movie_actor = models.TextField(default='', verbose_name=u"演员")
    movie_durations = models.TextField(default='', verbose_name=u"电影时长")
    movie_collect_count = models.IntegerField(default=0, verbose_name=u"收藏数")
    movie_mainland_pubdate = models.TextField(default='', verbose_name=u"主要上映日期")
    movie_images = models.TextField(default='', verbose_name=u"封面图片")
    record_time = models.DateTimeField(auto_now_add=True, verbose_name=u"录入时间")

    def __str__(self):
        return '%s - %s - %s - %s - %s - %s' % (self.movie_title, self.movie_rating, self.movie_year,
                                                self.movie_pubdates, self.movie_genres, self.movie_actor)

    class Meta:
        verbose_name = '豆瓣前250电影'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 豆瓣电影评分表
class MovieRatingDB(models.Model):
    rating = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='评分分数')
    movie_id = models.OneToOneField(CollectMovieDB, unique=True, to_field="movie_id", verbose_name='电影',
                                    on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.movie_id.title, self.rating)

    class Meta:
        verbose_name = '豆瓣电影评分表'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 豆瓣电影上映日期表
class MoviePubdateDB(models.Model):
    movie_id = models.OneToOneField(CollectMovieDB, unique=True, to_field="movie_id", verbose_name='电影',
                                    on_delete=models.CASCADE)
    pubdate = models.DateField(null=True, blank=True, verbose_name='上映日期')

    def __str__(self):
        return '%s - %s' % (self.movie_id.title, self.pubdate)

    class Meta:
        verbose_name = '豆瓣电影上映时间表'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 电影标签表
class MovieTagDB(models.Model):
    movie_id = models.ForeignKey(CollectMovieDB, to_field="movie_id", verbose_name='电影', on_delete=models.CASCADE)
    tag_type = models.CharField(max_length=100, db_index=True, blank=True, null=False, verbose_name='标签类型')
    tag_name = models.CharField(max_length=100, db_index=True, blank=True, null=False, verbose_name='标签名')

    def __str__(self):
        return '%s - %s - %s' % (self.movie_id.title, self.tag_type, self.tag_name)

    class Meta:
        verbose_name = '电影标签表'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 用户浏览记录表
class MovieBrows(models.Model):
    user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
    movie = models.ForeignKey(CollectMovieDB, to_field="movie_id", verbose_name='电影', on_delete=models.CASCADE)
    cookie_uuid = models.CharField(max_length=100, blank=True, null=False, verbose_name='COOKIE_UUID')
    brow_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='浏览时间')

    def __str__(self):
        return '%s - %s - %s - %s' % (self.user.user_name, self.movie.title, self.cookie_uuid, self.brow_time)

    class Meta:
        verbose_name = '用户浏览记录'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 用户搜索记录表
class MovieSearchs(models.Model):
    user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name='搜索类型')
    limit = models.IntegerField(verbose_name='搜索数量')
    page = models.IntegerField(verbose_name='搜索页数')
    content = models.CharField(max_length=100, blank=True, null=True, verbose_name='搜索内容')
    cookie_uuid = models.CharField(max_length=100, blank=True, null=False, verbose_name='COOKIE_UUID')
    search_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='搜索时间')

    def __str__(self):
        return '%s - %s - %s - %s- %s - %s - %s' % (self.user.user_name, self.type, self.page, self.limit,
                                                    self.content, self.cookie_uuid, self.search_time)

    class Meta:
        verbose_name = '用户搜索记录'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 用户对电影评分
class MovieRatings(models.Model):
    user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
    movie = models.ForeignKey(CollectMovieDB, to_field="movie_id", verbose_name='电影', on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name='评分分数')
    rating_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='评分时间')

    def __str__(self):
        return '%s - %s - %s - %s' % (self.user.user_name, self.movie.title, self.rating, self.rating_time)

    class Meta:
        verbose_name = '电影评分'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 用户对电影收藏
class MovieLikes(models.Model):
    user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
    movie = models.ForeignKey(CollectMovieDB, to_field="movie_id", verbose_name='电影', on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='收藏状态')
    like_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='收藏时间')

    def __str__(self):
        return '%s - %s - %s - %s' % (self.user.user_name, self.movie.title, self.status, self.like_time)

    class Meta:
        verbose_name = '电影收藏'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 用户对电影评论
class MovieComments(models.Model):
    user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
    movie = models.ForeignKey(CollectMovieDB, to_field="movie_id", verbose_name='电影', on_delete=models.CASCADE)
    userName = models.CharField(max_length=100, blank=True, null=True, verbose_name='用户昵称')
    movieName = models.CharField(max_length=100, blank=True, null=True, verbose_name='电影名称')
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='评论主题')
    content = models.TextField(verbose_name='评论内容')
    emotion = models.IntegerField(verbose_name='评论情感正负向')
    status = models.IntegerField(default=1, verbose_name='评论状态')
    ip = models.CharField(max_length=100, blank=True, null=True, verbose_name='操作IP')
    comment_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='浏览时间')

    def __str__(self):
        return '%s - %s - %s - %s - %s - %s' % (self.user.user_name, self.movie.title, self.status, self.title,
                                                self.emotion, self.comment_time)

    class Meta:
        verbose_name = '电影评论信息'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# class CollectMovieReviewsDB(models.Model):
#     reviews_id = models.IntegerField(unique=True, null=False,default=0,verbose_name=u"长评唯一标识")
#     reviews_movid_id = models.OneToOneField(CollectMovieDB, on_delete=models.CASCADE,verbose_name=u"电影唯一标识")
#     reviews_rating = models.IntegerField(default=0,verbose_name=u"评分")
#     reviews_useful_count = models.IntegerField(default=0,verbose_name=u"认为有用的评论")
#     reviews_content = models.TextField(default='',verbose_name=u"评论完整内容")
#     reviews_author_uid = models.TextField(default='',verbose_name=u"评论作者账号")
#     reviews_author_id = models.IntegerField(default=0,verbose_name=u"评论作者id")
#     reviews_author_name = models.TextField(default='',verbose_name=u"评论者昵称")
#     reviews_title = models.TextField(default='',verbose_name=u"评论标题")
#     reviews_share_url = models.TextField(default='',verbose_name=u"评论url")
#     reviews_summary = models.TextField(default='',verbose_name=u"评论简述内容")
#     reviews_useless_count = models.IntegerField(default=0,verbose_name=u"认为是无用的评论")
#     reviews_comments_count = models.IntegerField(default=0,verbose_name=u"评论数")
#     reviews_time = models.DateTimeField(auto_now_add=True,verbose_name=u"评论时间")
#
#     # 将属性和属性值转换成dict 列表生成式
#     def toDict(self):
#         return model_json.model_to_json(self)
#
#
# class MovieInfo(models.Model):
#     RATING_RANGE = (
#         MaxValueValidator(5),
#         MinValueValidator(0)
#     )
#     # moviename = models.CharField(max_length=1000, default='', verbose_name='电影名称')
#     # showyear = models.DateField(default=datetime.now, verbose_name='上映年份', null=True, blank=True)
#     # nation = models.CharField(max_length=255, default='', verbose_name='国家', null=True, blank=True)
#     # director = models.CharField(max_length=1000, default='', verbose_name='导演', null=True, blank=True)
#     # leadactors = models.CharField(max_length=1000, default='', verbose_name='主演', null=True, blank=True)
#     # screenwriter = models.CharField(max_length=255, default='', verbose_name='编剧', null=True, blank=True)
#     # picture = models.URLField(max_length=1000, verbose_name='海报', null=True, blank=True)
#     # averating = models.FloatField(default='', validators=RATING_RANGE, verbose_name='评分', null=True, blank=True)
#     # numrating = models.IntegerField( default=0, verbose_name='评分人数', null=True, blank=True)
#     # description = models.CharField(max_length=1000, default='', verbose_name='简介', null=True, blank=True)
#     # typelist = models.CharField(max_length=255, default='', verbose_name='类型', null=True, blank=True)
#     # backpost = models.CharField(max_length=15000, default='', null=True, blank=True)
#     moviename = models.CharField(max_length=1000, default='', verbose_name='电影名称')
#     # showyear = models.CharField(max_length=10, verbose_name='上映年份', null=True, blank=True)
#     releasedate = models.DateField(default=datetime.datetime.now, verbose_name='上映年份', null=True, blank=True)
#     nation = models.CharField(max_length=255, default='', verbose_name='国家', null=True, blank=True)
#     directors = models.CharField(max_length=1000, default='', verbose_name='导演', null=True, blank=True)
#     leadactors = models.CharField(max_length=1000, default='', verbose_name='主演', null=True, blank=True)
#     editors = models.CharField(max_length=255, default='', verbose_name='编剧', null=True, blank=True)
#     picture = models.URLField(max_length=1000, verbose_name='海报', null=True,
#                               blank=True,default='/static/images/t3.jpg')
#     averating = models.FloatField(default=0, validators=RATING_RANGE, verbose_name='评分', null=True, blank=True)
#     numrating = models.IntegerField(default=0, verbose_name='评分人数', null=True, blank=True)
#     description = models.TextField(default='', verbose_name='简介', null=True, blank=True)
#     typelist = models.ManyToManyField(MovieCategory, verbose_name='类型')
#     backpost = models.CharField(max_length=3000, default='', null=True, blank=True)
#
#
# class MovieCategory(models.Model):
#     category = models.CharField(max_length=100, default='', verbose_name='电影类型')
#     movienum = models.IntegerField(default=0, verbose_name='电影数量')
#
#     def __str__(self):
#         return self.category
#
#     class Meta:
#         verbose_name = '电影类型'
#         verbose_name_plural = verbose_name
#
#
# class MovieSimilar(models.Model):
#     item1 = models.IntegerField(default=0, verbose_name='电影id')
#     item2 = models.IntegerField(default=0, verbose_name='电影id')
#
#     # item1 = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
#     # item2 = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
#     similar = models.FloatField(default=0, verbose_name='相似度')
#
#     def __str__(self):
#         return '%d - %d - %lf' % (self.item1, self.item2, self.similar)
#
#     class Meta:
#         verbose_name = '电影相似度信息'
#         verbose_name_plural = verbose_name
#
#
# class Review(models.Model):
#     STAR_RANGE = [
#         MaxValueValidator(5),
#         MinValueValidator(0)
#     ]
#     user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
#     movie = models.ForeignKey(CollectMovieDB, verbose_name='电影', on_delete=models.CASCADE)
#     content = models.TextField(max_length=255, default='', verbose_name='评论', null=True, blank=True)
#     star = models.FloatField(default=0, validators=STAR_RANGE, verbose_name='星级')
#     reviewtime = models.DateTimeField(default=datetime.datetime.now, verbose_name='提交时间')
#
#     def __str__(self):
#         return '%s - %s - %lf' % (self.user.user_name, self.movie.title, self.star)
#
#     class Meta:
#         verbose_name = '用户回执'
#         verbose_name_plural = verbose_name
#
#
# class Default5Recommend(models.Model):
#     movie = models.ForeignKey(CollectMovieDB, verbose_name='电影', on_delete=models.CASCADE)
#     # movie = models.IntegerField(default=0, verbose_name='电影id')
#     redate = models.DateField(default=datetime.datetime.now, verbose_name='推荐时间')
#
#     def __str__(self):
#         return str(self.movie_id)
#
#     class Meta:
#         verbose_name = '默认电影推荐'
#         verbose_name_plural = verbose_name
#
#
# class Top5Recommend(models.Model):
#     # movieid = models.IntegerField(default=0, verbose_name='电影id')
#     # userid = models.IntegerField(default=0, verbose_name='用户id')
#     movie = models.ForeignKey(CollectMovieDB, verbose_name='电影', on_delete=models.CASCADE)
#     user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
#     rating = models.FloatField(default=0, verbose_name='评分')
#
#     def __str__(self):
#         return '%s - %s -%lf' % (self.user, self.movie, self.rating)
#         # return '%s - %s -%lf' % (self.userid, self.movieid, self.rating)
#
#     class Meta:
#         verbose_name = '用户推荐信息'
#         verbose_name_plural = verbose_name
#
#
# class Rating(models.Model):
#     RATING_RANGE = (
#         MaxValueValidator(5),
#         MinValueValidator(0)
#     )
#     movie = models.ForeignKey(CollectMovieDB, verbose_name='电影', on_delete=models.CASCADE)
#     user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
#     rating = models.FloatField(default=0, validators=RATING_RANGE, verbose_name='评分', null=True, blank=True)
#     ds = models.BigIntegerField(default=time.mktime(datetime.datetime.now().timetuple()), verbose_name='时间戳')
#
#     def __str__(self):
#         return '%s - %s - %lf' % (self.user, self.movie, self.rating)
#
#     class Meta:
#         verbose_name = '用户评分'
#         verbose_name_plural = '用户评分'
#
#
# class AlsTable(models.Model):
#     RATING_RANGE = (
#         MaxValueValidator(5),
#         MinValueValidator(0)
#     )
#     user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
#     movie = models.ForeignKey(CollectMovieDB, verbose_name='电影', on_delete=models.CASCADE)
#     rating = models.FloatField(default=0, validators=RATING_RANGE, verbose_name='评分', null=True, blank=True)
