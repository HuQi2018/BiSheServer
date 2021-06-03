from django.contrib import admin

# Register your models here.
from api.models import districts, IndexFocus
from user.models import UsersDetail, UsersBase, UsersPerfer, UserCookie, UserTag, UserMovieRecommend
from movie.models import CollectMovieDB, CollectMovieTypeDB, CollectTop250MovieDB, MovieRatingDB, MoviePubdateDB, \
    MovieTagDB, MovieBrows, MovieSearchs, MovieRatings, MovieLikes, MovieComments


# class MyAdminSite(admin.AdminSite):
#     site_header = '电影推荐资源管理系统'  # 此处设置页面显示标题
#     site_title = '电影推荐资源管理系统'  # 此处设置页面头部标题
#
#
# admin_site = MyAdminSite(name='management')
admin.site.site_header = '电影推荐资源管理系统'
admin.site.site_title = '电影推荐资源管理系统'


class UserInline(admin.TabularInline):
    model = UsersDetail
    list_display = ('user_age', 'user_birthday', 'user_address', 'user_province', 'user_city',
                    'user_district', 'user_prefer', 'user_hobbies', 'user_created')


@admin.register(UsersBase)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserInline]  # Inline 内联形式

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user_name', 'user_role', 'user_status', 'user_gender', 'user_phone', 'user_img',
                    'user_uname', 'user_mail', 'user_reg_step')

    # 可搜索字段
    search_fields = ('id', 'user_name', 'user_role', 'user_status', 'user_gender', 'user_phone',
                     'user_uname', 'user_mail', 'user_reg_step')

    # 列表过滤
    list_filter = ['user_role', 'user_status', 'user_gender', 'user_reg_step']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-id']

    # list_editable 设置默认可编辑字段
    list_editable = ['user_name', 'user_role', 'user_status', 'user_gender', 'user_phone', 'user_img',
                     'user_uname', 'user_mail', 'user_reg_step']


@admin.register(UsersDetail)
class UsersDetailAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user_id', 'user_age', 'user_birthday', 'user_address', 'user_province', 'user_city',
                    'user_district', 'user_prefer', 'user_hobbies', 'user_created')

    # 可搜索字段
    search_fields = ('id', 'user_id', 'user_age', 'user_birthday', 'user_address', 'user_province', 'user_city',
                     'user_district', 'user_prefer', 'user_hobbies', 'user_created')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-id', 'user_created']

    # 列表过滤
    list_filter = ['user_age']

    # list_editable 设置默认可编辑字段
    list_editable = ['user_id', 'user_age', 'user_birthday', 'user_address', 'user_province', 'user_city',
                     'user_district', 'user_prefer', 'user_hobbies']

    # fk_fields 设置显示外键字段
    fk_fields = ('user_id__user_name',)

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['user_id']

# admin.site.register(UsersBase, UserAdmin)
# admin.site.register([UsersDetail, UsersPerfer, UserCookie, UserTag])
# admin.site.register([CollectMovieDB, CollectMovieTypeDB, CollectTop250MovieDB, MovieRatingDB, MoviePubdateDB,
#                      MovieTagDB, MovieBrows, MovieSearchs, MovieRatings, MovieLikes, MovieComments])
# admin.site.register([districts, IndexFocus])


@admin.register(CollectMovieDB)
class CollectMovieDBAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'movie_id', 'title', 'pubdate', 'year', 'genres', 'countries')

    # 可搜索字段
    search_fields = ['movie_id', 'title', 'pubdate', 'year', 'genres', 'countries']

    # 列表过滤
    list_filter = ['year']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-year', '-pubdate')

    # list_editable 设置默认可编辑字段
    list_editable = ['movie_id', 'title']


@admin.register(CollectTop250MovieDB)
class CollectTop250MovieDBAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'movie_id', 'movie_title', 'movie_year', 'movie_pubdates', 'movie_genres', 'movie_actor')

    # 可搜索字段
    search_fields = ['movie_id', 'movie_title', 'movie_year', 'movie_pubdates', 'movie_genres', 'movie_actor']

    # 列表过滤
    list_filter = ['movie_year']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-movie_rating', '-movie_year')

    # list_editable 设置默认可编辑字段
    list_editable = ['movie_id', 'movie_title', 'movie_genres']


@admin.register(MovieRatingDB)
class MovieRatingDBAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'movie_id', 'rating')

    # 可搜索字段
    search_fields = ['movie_id__movie_id', 'movie_id__title', 'rating']

    # 列表过滤
    # list_filter = ['rating', 'movie_id__year']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-rating',)

    # list_editable 设置默认可编辑字段
    list_editable = ['movie_id', 'rating']

    # fk_fields 设置显示外键字段
    fk_fields = ('movie_id__title',)

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['movie_id']


@admin.register(MoviePubdateDB)
class MoviePubdateDBAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'movie_id', 'pubdate')

    # 可搜索字段
    search_fields = ['movie_id__movie_id', 'movie_id__title', 'pubdate']

    # 列表过滤
    # list_filter = ['pubdate']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-pubdate']

    # list_editable 设置默认可编辑字段
    list_editable = ['movie_id', 'pubdate']

    # fk_fields 设置显示外键字段
    fk_fields = ('movie_id__title',)

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['movie_id']


@admin.register(MovieTagDB)
class MovieTagDBAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'movie_id', 'tag_type', 'tag_name')

    # 可搜索字段
    search_fields = ['movie_id__movie_id', 'movie_id__title', 'tag_type', 'tag_name']

    # 列表过滤
    list_filter = ['tag_type']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # list_editable 设置默认可编辑字段
    list_editable = ['movie_id', 'tag_type', 'tag_name']

    # fk_fields 设置显示外键字段
    fk_fields = ('movie_id__title',)

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['movie_id']


@admin.register(MovieBrows)
class MovieBrowsAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user', 'movie', 'cookie_uuid', 'brow_time')

    # 可搜索字段
    search_fields = ['cookie_uuid', 'movie__movie_id', 'movie__title', 'user__user_name']

    # 列表过滤
    list_filter = ['cookie_uuid']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-brow_time']

    # list_editable 设置默认可编辑字段
    list_editable = ['user', 'movie', 'cookie_uuid', 'brow_time']

    # fk_fields 设置显示外键字段
    fk_fields = ('movie__title', 'user__user_name')

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['movie', 'user']


@admin.register(MovieSearchs)
class MovieSearchsAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user', 'type', 'limit', 'page', 'cookie_uuid', 'search_time')

    # 可搜索字段
    search_fields = ['cookie_uuid', 'user__user_name']

    # 列表过滤
    list_filter = ['type', 'cookie_uuid']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-search_time']

    # list_editable 设置默认可编辑字段
    list_editable = ['user', 'type', 'cookie_uuid', 'search_time']

    # fk_fields 设置显示外键字段
    fk_fields = ('user__user_name',)

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['user']


@admin.register(MovieRatings)
class MovieRatingsAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user', 'movie', 'rating', 'rating_time')

    # 可搜索字段
    search_fields = ['user__user_name', 'movie__movie_id', 'movie__title', 'rating']

    # 列表过滤
    list_filter = ['rating']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-rating_time']

    # list_editable 设置默认可编辑字段
    list_editable = ['user', 'movie', 'rating', 'rating_time']

    # fk_fields 设置显示外键字段
    fk_fields = ('movie__title', 'user__user_name')

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['movie', 'user']


@admin.register(MovieLikes)
class MovieLikesAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user', 'movie', 'status', 'like_time')

    # 可搜索字段
    search_fields = ['user__user_name', 'movie__movie_id', 'movie__title', 'status', 'like_time']

    # 列表过滤
    list_filter = ['status']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-like_time']

    # list_editable 设置默认可编辑字段
    list_editable = ['user', 'movie', 'status', 'like_time']

    # fk_fields 设置显示外键字段
    fk_fields = ('movie__title', 'user__user_name')

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['movie', 'user']


@admin.register(MovieComments)
class MovieCommentsAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user', 'movie', 'userName', 'movieName', 'title', 'emotion', 'ip', 'status', 'comment_time')

    # 可搜索字段
    search_fields = ['user__user_name', 'movie__movie_id', 'movie__title', 'userName', 'movieName', 'title', 'ip',
                     'status', 'comment_time']

    # 列表过滤
    list_filter = ['status', 'movieName', 'userName', 'ip', 'emotion']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-comment_time']

    # list_editable 设置默认可编辑字段
    list_editable = ['user', 'movie', 'userName', 'movieName', 'title', 'ip', 'status', 'comment_time']

    # fk_fields 设置显示外键字段
    fk_fields = ('movie__title', 'user__user_name')

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['movie', 'user']


@admin.register(IndexFocus)
class IndexFocusAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'movie_id', 'show_id', 'movie_img', 'movie_content', 'status', 'create_time')

    # 可搜索字段
    search_fields = ['movie_id__movie_id', 'movie_id__title', 'show_id', 'movie_content', 'status', 'create_time']

    # 列表过滤
    list_filter = ['status']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['show_id', '-create_time']

    # list_editable 设置默认可编辑字段
    list_editable = ['movie_id', 'show_id', 'movie_img', 'movie_content', 'status']

    # fk_fields 设置显示外键字段
    fk_fields = ('movie_id__title',)

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['movie_id']


@admin.register(UserCookie)
class UserCookieAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user', 'cookie_uuid', 'user_ip', 'create_time', 'quit_time')

    # 可搜索字段
    search_fields = ['user__user_name', 'cookie_uuid', 'user_ip', 'create_time', 'quit_time']

    # 列表过滤
    list_filter = ['cookie_uuid', 'user_ip']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-create_time', '-quit_time']

    # list_editable 设置默认可编辑字段
    list_editable = ['user', 'cookie_uuid', 'user_ip', 'quit_time']

    # fk_fields 设置显示外键字段
    fk_fields = ('user__user_name',)

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['user']


@admin.register(UserTag)
class UserTagAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user', 'tag_type', 'tag_name', 'tag_weight', 'create_time')

    # 可搜索字段
    search_fields = ['user__user_name', 'tag_type', 'tag_name', 'tag_weight']

    # 列表过滤
    list_filter = ['tag_type', 'tag_weight']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['-tag_type', '-create_time']

    # list_editable 设置默认可编辑字段
    list_editable = ['user', 'tag_type', 'tag_name', 'tag_weight']

    # fk_fields 设置显示外键字段
    fk_fields = ('user__user_name',)

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['user']


@admin.register(districts)
class DistrictsAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'parent', 'code', 'name')

    # 可搜索字段
    search_fields = ['parent', 'code', 'name']

    # 列表过滤
    # list_filter = ['parent', 'code']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # list_editable 设置默认可编辑字段
    list_editable = ['parent', 'code', 'name']


@admin.register(UsersPerfer)
class UsersPerferAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user_prefer')

    # 可搜索字段
    search_fields = ['user_prefer']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # list_editable 设置默认可编辑字段
    list_editable = ['user_prefer']


@admin.register(CollectMovieTypeDB)
class CollectMovieTypeDBAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'movie_type')

    # 可搜索字段
    search_fields = ['movie_type']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # list_editable 设置默认可编辑字段
    list_editable = ['movie_type']


@admin.register(UserMovieRecommend)
class UserMovieRecommendAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user', 'movie_id_li', 'create_time')

    # 可搜索字段
    search_fields = ['user__user_name', 'movie_id_li']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ['user']

    # list_editable 设置默认可编辑字段
    list_editable = ['user', 'movie_id_li']

    # fk_fields 设置显示外键字段
    fk_fields = ('user__user_name',)

    # 让关联的表的数据 暂时不加载
    raw_id_fields = ['user']

# 列表默认显示
# list_display = ['id', 'username', 'nick_name', 'first_name', 'last_name', 'gender', 'age', 'email', 'is_staff',
#                 'is_active',
#                 'location', 'date_joined']
# # 搜索范围
# search_fields = ['id', 'username', 'nick_name', 'first_name', 'last_name', 'gender', 'age', 'email', 'is_staff',
#                  'is_active',
#                  'location']
# # 列表过滤
# list_filter = ['id', 'username', 'nick_name', 'first_name', 'last_name', 'gender', 'age', 'email', 'is_staff',
#                'is_active',
#                'location', 'date_joined']
# # 只读
# # readonly_fields = ['is_staff', 'is_active', 'date_joined']
# # 直接编辑
# list_editable = ['username', 'nick_name', 'first_name', 'last_name', 'gender', 'age', 'email', 'is_staff',
#                  'is_active',
#                  'location']


# class TagInline(admin.TabularInline):
#     model = Tag
#
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ('name', 'age', 'email')  # 显示多列信息
#     search_fields = ('name',)  # 增加所搜框
#     inlines = [TagInline]  # Inline 内联形式
#     fieldsets = (
#         ['Main',{
#             'fields':('name','email'),
#         }],
#         ['Advance',{
#             'classes': ('collapse',), # CSS
#             'fields': ('age',),
#         }]
#     )
#
# class UserInline(admin.TabularInline):
#     model = UsersDetail
#
# class UserAdmin(admin.ModelAdmin):
#     inlines = [UserInline]  # Inline 内联形式
#     # fieldsets = (
#     #     ['Main',{
#     #         'fields':('user_name','user_role','user_status','user_mail','user_phone'),
#     #     }],
#     #     ['Advance',{
#     #         'classes': ('collapse',), # CSS
#     #         'fields': ('user_gender',),
#     #     }]
#     # )
#
# # admin.site.register(Contact, ContactAdmin)
# # admin.site.register(UsersBase, UserAdmin)
# # admin.site.register([Test, Tag, UserInfo, UsersDetail])
# # admin.site.register([Test, Test1, Contact, Tag, UserInfo])
