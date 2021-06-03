import datetime

from django.db import models


# 中国省市地区表
from movie.models import CollectMovieDB


class districts(models.Model):
    parent = models.IntegerField(default=0, verbose_name=u"父区域代号")
    code = models.IntegerField(default=0, verbose_name=u"子区域代号")
    name = models.CharField(max_length=100, default=0, verbose_name=u"区域名称")

    def __str__(self):
        return '%s - %s - %s' % (self.parent, self.code, self.name)

    class Meta:
        verbose_name = '中国省市地区表'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__


# 首页轮播图
class IndexFocus(models.Model):
    movie_id = models.ForeignKey(CollectMovieDB, to_field="movie_id", verbose_name='电影', on_delete=models.CASCADE)
    show_id = models.IntegerField(default=0, verbose_name=u"显示顺序")
    movie_img = models.ImageField(upload_to='static/images/focus/', default='static/images/focus/4136f145453342.jpg',
                                  verbose_name=u"电影海报图片地址")
    movie_content = models.CharField(max_length=100, default=0, verbose_name=u"描述")
    status = models.IntegerField(default=1, verbose_name=u"显示状态")
    create_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')

    def __str__(self):
        return '%s - %s - %s - %s - %s' % (self.movie_id, self.show_id, self.movie_img, self.movie_content, self.status)

    class Meta:
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
