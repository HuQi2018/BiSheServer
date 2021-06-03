from django.db import models

from api import model_json


# 用户喜好标签表
class UsersPerfer(models.Model):
    user_prefer = models.CharField(max_length=100, unique=True, default="", verbose_name=u"用户喜好")

    def __str__(self):
        return self.user_prefer

    class Meta:
        verbose_name = '用户喜好标签名表'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__


# 用户基本信息表
class UsersBase(models.Model):
    user_name = models.CharField(max_length=100, unique=True, null=False, verbose_name=u"用户登录名",
                                 error_messages={"min_length": "长度不足", "required": "该字段不能为空!"})
    user_passwd = models.CharField(max_length=100, default=0, verbose_name=u"用户密码")
    user_role = models.CharField(max_length=100, default=1, verbose_name=u"用户角色")  # 2管理员  1普通用户
    user_status = models.CharField(max_length=100, default=0, verbose_name=u"用户状态")  # 0未验证账户 1正常账户
    user_gender = models.CharField(max_length=100, default=0, null=True, verbose_name=u"用户性别")  # 1男 2女
    user_phone = models.CharField(max_length=11, unique=True, null=True, verbose_name=u"用户手机号")
    user_img = models.CharField(max_length=100, default='static/images/user.jpg', verbose_name=u"用户头像")
    # user_img = models.ImageField(upload_to='static/images/avatars/', default='static/images/user.jpg',
    # verbose_name=u"用户头像")
    user_uname = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"用户昵称")
    user_mail = models.EmailField(max_length=100, unique=True, verbose_name=u"用户邮箱")
    user_reg_step = models.IntegerField(default=0, verbose_name=u"用户注册到第几步")

    def __unicode__(self):
        return self.id

    def __str__(self):
        # return str(self.id)
        return '%s - %s - %s' % (self.user_name, self.user_status, self.user_mail)

    class Meta:
        verbose_name = '用户基本信息表'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 用户详细信息表
class UsersDetail(models.Model):
    user_id = models.OneToOneField(UsersBase, on_delete=models.CASCADE, verbose_name=u"用户唯一标识")
    user_age = models.IntegerField(blank=True, null=True, verbose_name=u"用户年龄")
    user_birthday = models.DateField(blank=True, null=True, verbose_name=u"用户生日")
    user_address = models.TextField(max_length=500, blank=True, null=True, verbose_name=u"用户地址")
    user_province = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"所属省市")
    user_city = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"所属城市")
    user_district = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"区县")
    user_created = models.DateTimeField(auto_now_add=True, verbose_name=u"用户注册时间")
    user_prefer = models.TextField(blank=True, null=True, verbose_name=u"用户标签")
    user_hobbies = models.TextField(blank=True, null=True, verbose_name=u"用户爱好")

    def __str__(self):
        # return self.user_id
        return '%s - %s - %s - %s - %s - %s' % (self.user_id, self.user_id.user_name, self.user_age, self.user_address,
                                                self.user_birthday, self.user_created)

    class Meta:
        verbose_name = '用户详细信息表'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 用户cookie与user关联表
class UserCookie(models.Model):
    user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
    cookie_uuid = models.CharField(max_length=100, blank=True, null=False, verbose_name='COOKIE_UUID')
    user_agent = models.TextField(verbose_name='HTTP_USER_AGENT')
    user_ip = models.CharField(max_length=100, blank=True, null=True, verbose_name='登录IP')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
    quit_time = models.DateTimeField(null=True, blank=True, verbose_name='退出时间')

    def __str__(self):
        return '%s - %s - %s - %s - %s' % (self.user.user_name, self.cookie_uuid, self.user_ip,
                                           self.create_time, self.quit_time)

    class Meta:
        verbose_name = 'COOKIE记录'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 用户标签表
class UserTag(models.Model):
    user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
    tag_type = models.CharField(max_length=100, db_index=True, blank=True, null=False, verbose_name='标签类型')
    tag_name = models.CharField(max_length=100, db_index=True, blank=True, null=False, verbose_name='标签名')
    tag_weight = models.IntegerField(default=0, verbose_name='标签权重')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return '%s - %s - %s - %s - %s' % (self.user.user_name, self.tag_type, self.tag_name, self.tag_weight,
                                           self.create_time)

    class Meta:
        verbose_name = '用户标签表'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)


# 用户电影推荐表
class UserMovieRecommend(models.Model):
    user = models.ForeignKey(UsersBase, verbose_name='用户', on_delete=models.CASCADE)
    movie_id_li = models.TextField(verbose_name='电影id列表')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return '%s - %s - %s' % (self.user.user_name, self.movie_id_li, self.create_time)

    class Meta:
        verbose_name = '用户电影推荐表'
        verbose_name_plural = verbose_name

    # 将属性和属性值转换成dict 列表生成式
    def toDict(self):
        return model_json.model_to_json(self)
