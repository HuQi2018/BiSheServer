import ast
import threading
# from multiprocessing import Process

from django.db.models import Q

from movie.models import CollectMovieDB
from user.models import UserTag
from . import user_api
from phone import Phone

User = user_api.User()
add_user_tag = User.add_user_tag
modify_user_tag = User.modify_user_tag


# 线程延迟工作
def delay_work(time, work):
    threading.Timer(time, work).start()


# 获取电影标签
def get_movie_tag(movie_id):
    res_tag = []
    movie_data_tags = CollectMovieDB.objects.filter(movie_id=movie_id).values("tags", "genres", "countries",
                                                                              "languages", "year").first()
    # print(movie_data_tags)
    # tags = movie_data_tags["tags"]
    genres = movie_data_tags["genres"]
    countries = movie_data_tags["countries"]
    languages = movie_data_tags["languages"]
    year = movie_data_tags["year"]
    # if tags:
    #     tags = ast.literal_eval(tags)
    #     for tag in tags:
    #         # res_tag.append("info_movie_tag--"+tag)
    #         res_tag.append(tag)
    if genres:
        genres = ast.literal_eval(genres)
        for genre in genres:
            res_tag.append("info_movie_type--"+genre)
            # res_tag.append(genre)
    if countries:
        countries = ast.literal_eval(countries)
        for country in countries:
            res_tag.append("info_movie_tag--"+country)
            # res_tag.append(country)
    if languages:
        languages = ast.literal_eval(languages)
        for language in languages:
            res_tag.append("info_movie_tag--"+language)
            # res_tag.append(language)
    if year:
        res_tag.append("info_movie_tag--"+str(year))
        # res_tag.append(year)
    # print(res_tag)
    return res_tag


# 用户信息打标签，注册和修改用户信息时修改
def user_info_tag(key):

    key = ast.literal_eval(key)
    if key.get("tag_weight"):
        tag_weight = key["tag_weight"]
    else:
        tag_weight = 5
    # 电话归属地标签 info_phone_city  使用邮编码
    if key.get("user_phone"):
        phone_info = Phone().find(key["user_phone"])
        # zip_code  phone_info['province']+'-'+phone_info['city']   phone_info['zip_code']
        modify_user_tag(key["user_id"], "info_phone_city", phone_info['province']+'-'+phone_info['city'], tag_weight)

    # 性别标签       info_sex
    if key.get("user_gender"):
        modify_user_tag(key["user_id"], "info_sex", key["user_gender"], tag_weight)

    # 城市标签       info_city
    if key.get("user_city"):
        modify_user_tag(key["user_id"], "info_city", key["user_city"], tag_weight)

    # 年龄标签       info_age
    if key.get("user_age"):
        modify_user_tag(key["user_id"], "info_age", key["user_age"], tag_weight)

    # 省市标签       info_province
    if key.get("user_province"):
        modify_user_tag(key["user_id"], "info_province", key["user_province"], tag_weight)

    # 喜欢的电影类型标签   info_movie_type
    if key.get("user_prefer"):
        user_prefers = key["user_prefer"].split(",")
        user_tag = list(UserTag.objects.filter(Q(user_id=key["user_id"]) & Q(tag_type="info_movie_type"))
                        .values_list("tag_name", flat=True))
        # user_tag = key["user_tag"]
        other_tags = [i for i in user_tag if i not in user_prefers]  # 求差集
        for user_prefer in user_prefers:
            modify_user_tag(key["user_id"], "info_movie_type", user_prefer, tag_weight)
        for other_tag in other_tags:  # 取消本次未选中的标签，将其权值赋为0
            modify_user_tag(key["user_id"], "info_movie_type", other_tag, 0)

    # 爱好标签        info_hobbies
    if key.get("user_hobbies"):
        user_hobbies = key["user_hobbies"].split(",")
        user_tag = list(UserTag.objects.filter(Q(user_id=key["user_id"]) & Q(tag_type="info_hobbies"))
                        .values_list("tag_name", flat=True))
        # user_tag = key["user_tag"]
        other_tags = [i for i in user_tag if i not in user_hobbies]  # 求差集
        for user_hobbie in user_hobbies:
            modify_user_tag(key["user_id"], "info_hobbies", user_hobbie, tag_weight)
        for other_tag in other_tags:  # 取消本次未选中的标签，将其权值赋为0
            modify_user_tag(key["user_id"], "info_hobbies", other_tag, 0)


# 用户收藏操作打标签
def user_like_tag(key):

    key = ast.literal_eval(key)
    movie_tags = get_movie_tag(key["movie_id"])
    # movie_tags = key["movie_tags"]

    if key["tag_sign"] == "init":  # 电影第一次收藏
        modify_user_tag(key["user_id"], "like_movie_id", key["movie_id"], 5)
        for movie_tag in movie_tags:
            movie_tag = movie_tag.split("--")
            modify_user_tag(key["user_id"], movie_tag[0], movie_tag[1], "+3")

    elif key["tag_sign"] == "like":  # 电影取消收藏之后的再次收藏
        modify_user_tag(key["user_id"], "like_movie_id", key["movie_id"], 5)
        for movie_tag in movie_tags:
            movie_tag = movie_tag.split("--")
            modify_user_tag(key["user_id"], movie_tag[0], movie_tag[1], "+3")

    elif key["tag_sign"] == "cancel":  # 电影取消收藏
        modify_user_tag(key["user_id"], "like_movie_id", key["movie_id"], 0)
        for movie_tag in movie_tags:
            movie_tag = movie_tag.split("--")
            modify_user_tag(key["user_id"], movie_tag[0], movie_tag[1], "-3")


# 用户评分操作打标签
def user_rating_tag(key):

    key = ast.literal_eval(key)
    movie_tags = get_movie_tag(key["movie_id"])
    # movie_tags = key["movie_tags"]

    if key["tag_sign"] == "init":  # 电影第一次评分
        modify_user_tag(key["user_id"], "rating_movie_id", key["movie_id"], str(key["rating"]))
        for movie_tag in movie_tags:
            movie_tag = movie_tag.split("--")
            modify_user_tag(key["user_id"], movie_tag[0], movie_tag[1], "+" + str(key["rating"]))

    elif key["tag_sign"] == "again":  # 电影再次评分
        rating = str(key["rating"] - key["old_rating"])
        modify_user_tag(key["user_id"], "rating_movie_id", key["movie_id"], rating)
        for movie_tag in movie_tags:
            movie_tag = movie_tag.split("--")
            modify_user_tag(key["user_id"], movie_tag[0], movie_tag[1], rating)


# 用户评论操作打标签
def user_comment_tag(key):

    key = ast.literal_eval(key)
    movie_tags = get_movie_tag(key["movie_id"])
    # movie_tags = key["movie_tags"]
    emotion = int(int(key["emotion"])/10)-5
    if key["tag_sign"] == "add":  # 添加电影评论
        modify_user_tag(key["user_id"], "comment_movie_id", key["movie_id"], str(emotion))
        for movie_tag in movie_tags:
            movie_tag = movie_tag.split("--")
            modify_user_tag(key["user_id"], movie_tag[0], movie_tag[1], str(emotion))

    elif key["tag_sign"] == "delete":  # 删除电影评论
        modify_user_tag(key["user_id"], "comment_movie_id", key["movie_id"], str(-emotion))
        for movie_tag in movie_tags:
            movie_tag = movie_tag.split("--")
            modify_user_tag(key["user_id"], movie_tag[0], movie_tag[1], str(-emotion))


# 用户搜索操作打标签
def user_search_tag(key):

    key = ast.literal_eval(key)
    search_key = key["search_key"]
    if key['movie_type'] == "genres":
        modify_user_tag(key["user_id"], "info_movie_type", search_key, "+3")
    else:
        modify_user_tag(key["user_id"], "info_movie_tag", search_key, "+3")


# 用户浏览操作打标签
def user_brow_tag(key):

    key = ast.literal_eval(key)
    movie_tags = get_movie_tag(key["movie_id"])
    # movie_tags = key["movie_tags"]
    for movie_tag in movie_tags:
        movie_tag = movie_tag.split("--")
        modify_user_tag(key["user_id"], movie_tag[0], movie_tag[1], "+1")


class TagThread(threading.Thread):
    def __init__(self, func, args):
        self.func = func
        self.kwargs = args
        threading.Thread.__init__(self)

    def run(self):
        eval(str(self.func)+'("'+str(self.kwargs)+'")')


def tag_thread_work(add_type, **kwargs):
    allow_type = ["user_info_tag", "user_like_tag", "user_rating_tag", "user_comment_tag", "user_brow_tag",
                  "user_search_tag"]
    if add_type in allow_type:
        TagThread(func=add_type, args=kwargs).start()
    # eval(func)()
    # if add_type == "user_info_tag":  # 用户注册、用户修改信息
    #     # if kwargs["user_prefer"]:
    #     #     user_tag = list(UserTag.objects.filter(user_id=kwargs["user_id"], tag_type="info_movie_type")
    #     #                     .values_list("tag_name"))
    #     #     kwargs["user_tag"] = user_tag
    #     # if kwargs["user_hobbies"]:
    #     #     user_tag = list(UserTag.objects.filter(user_id=kwargs["user_id"], tag_type="info_hobbies")
    #     #                     .values_list("tag_name"))
    #     #     kwargs["user_tag"] = user_tag
    #     TagThread(func="user_info_tag", args=kwargs).start()
    #     # Process(target=user_info_tag, args=kwargs).start()
    # elif add_type == "user_like_tag":  # 用户收藏
    #     # movie_tags = get_movie_tag(kwargs["movie_id"])
    #     # kwargs["movie_tags"] = movie_tags
    #     # Process(target=user_like_tag, args=kwargs).start()
    #     TagThread(func="user_like_tag", args=kwargs).start()
    # elif add_type == "user_rating_tag":  # 用户评分
    #     # movie_tags = get_movie_tag(kwargs["movie_id"])
    #     # kwargs["movie_tags"] = movie_tags
    #     # Process(target=user_rating_tag, args=kwargs).start()
    #     TagThread(func="user_rating_tag", args=kwargs).start()
    # elif add_type == "user_comment_tag":  # 用户评论
    #     # movie_tags = get_movie_tag(kwargs["movie_id"])
    #     # kwargs["movie_tags"] = movie_tags
    #     # Process(target=user_comment_tag, args=kwargs).start()
    #     TagThread(func="user_comment_tag", args=kwargs).start()
    # elif add_type == "user_search_tag":  # 用户搜索
    #     TagThread(func="user_search_tag", args=kwargs).start()
    #     # Process(target=user_search_tag, args=kwargs).start()
    # elif add_type == "user_brow_tag":  # 用户浏览
    #     # movie_tags = get_movie_tag(kwargs["movie_id"])
    #     # kwargs["movie_tags"] = movie_tags
    #     # Process(target=user_brow_tag, args=kwargs).start()
    #     TagThread(func="user_brow_tag", args=kwargs).start()
