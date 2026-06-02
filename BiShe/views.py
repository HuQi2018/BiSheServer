import json
import random
import uuid
from functools import wraps

from django.contrib.auth import authenticate, login
from django.shortcuts import render

from api import movie_api, user_api, api, delay_work
from movie.models import MovieBrows

from user.models import UsersBase, UsersDetail

Movie = movie_api.Movie()
User = user_api.User()

isNotLogin = User.isNotLogin
movie_tag = Movie.get_movie_tag
getHobbiesTag = User.getHobbiesTag
getUserPreferTag = User.getUserPreferTag

movie_search = Movie.movie_search
movie_search_by_id = Movie.movie_search_by_id
movie_search_by_web = Movie.movie_search_by_web

get_user_movie_comment = Movie.get_user_movie_comment
get_movie_comment = Movie.get_movie_comment
get_user_comment = Movie.get_user_comment
get_user_search = Movie.get_user_search
get_user_movie_rating = Movie.get_user_movie_rating
get_user_movie_brow = Movie.get_user_movie_brow
get_user_movie_like = Movie.get_user_movie_like
get_user_movie_5_like = Movie.get_user_movie_5_like
get_user_movie_5_brow = Movie.get_user_movie_5_brow
get_movie_5_cai = Movie.get_movie_5_cai
get_user_movie_5_cai = Movie.get_user_movie_5_cai
get_visiter_movie_5_brow = Movie.get_visiter_movie_5_brow
get_user_like = Movie.get_user_like
get_movie_douban_top = Movie.get_movie_douban_top
get_movie_douban_new = Movie.get_movie_douban_new
get_index_tag_movie = Movie.get_index_tag_movie

default_tag = ["动作", "科幻", "爱情", "喜剧"]
# data = dict()


def index(request):
    cookie_uuid = request.COOKIES.get("uuid")

    user_id = request.session.get("user_id") if request.session.get("user_id") else 2
    data = page_nav(request)
    data["index_focus"] = api.Api().index_focus()
    # 获取前十个高分电影
    data["movie_douban_top"] = get_movie_douban_top(1, 10)
    # 获取5个最新上映的电影
    data['movie_douban_new'] = get_movie_douban_new()
    data['movie_index_tag'] = [{"tag": "", "data": []} for _ in range(4)]
    if user_id == 2:
        data['movie_index_tag'] = data['movie_nav_tag']
        # for i, tag in enumerate(default_tag):
        #     data['movie_index_tag'][i]["tag"] = tag
        #     data['movie_index_tag'][i]["data"] = get_index_tag_movie(tag)
        # data['movie_nav_tag'] = []
    else:
        userPerferTag = getUserPreferTag(user_id)
        user_tag = userPerferTag.split(",") if userPerferTag != '' and userPerferTag is not None else []
        if len(user_tag) < 4:
            # 不够4个就用default_tag填补，求差集
            other_tag = [i for i in default_tag if i not in user_tag]
            for ta in range(4 - len(user_tag)):
                user_tag.append(other_tag[ta])
        # 随机选4各类别进行显示
        for (i, tag) in enumerate(random.sample(user_tag, 4)):
            data['movie_index_tag'][i]["tag"] = tag
            data['movie_index_tag'][i]["data"] = get_index_tag_movie(tag_name=tag, user_id=user_id)
        # data['movie_nav_tag'] = []response.set_cookie('username','xiaoming')

    if not cookie_uuid:
        cookie_uuid = uuid.uuid4().hex
        request.COOKIES["uuid"] = cookie_uuid
        response = render(request, 'index.html', {"page": "index.html", "data": data})
        response.set_cookie("uuid", cookie_uuid)
    else:
        response = render(request, 'index.html', {"page": "index.html", "data": data})
    return response


def register(request):
    data = page_nav(request)
    data['user_hobbies'] = getHobbiesTag()
    return render(request, 'register.html', {"page": "register.html", "data": data})


def category(request):
    data = page_nav(request)
    return render(request, 'category.html', {"page": "category.html", "data": data})


def search(request):
    data = page_nav(request)
    data["movie_data"] = json.dumps(movie_search(request))
    cookie_uuid = request.COOKIES.get("uuid")
    if not cookie_uuid:
        cookie_uuid = uuid.uuid4().hex
        request.COOKIES["uuid"] = cookie_uuid
    response = render(request, 'search.html', {"page": "search.html", "data": data})
    response.set_cookie("uuid", cookie_uuid)
    return response


def movie(request):
    user_id = request.session.get("user_id") if request.session.get("user_id") else 2
    movie_id = request.GET.get("id")
    data = page_nav(request)
    data["user_movie_comment_id"] = []
    data["user_movie_rating"] = []
    data["user_movie_like"] = []
    # 获取用户对电影的评论id，供判断删除评论使用
    if user_id != 2:
        # 获取用户对电影评论id
        data["user_movie_comment_id"] = get_user_movie_comment(user_id=user_id, movie_id=movie_id, is_list=1)
        # 获取用户对电影评分信息
        data["user_movie_rating"] = get_user_movie_rating(user_id=user_id, movie_id=movie_id, is_list=1)
        # 获取用户对电影收藏信息
        data["user_movie_like"] = get_user_movie_like(user_id=user_id, movie_id=movie_id, is_list=1)
    # 获取电影的所有评论
    data["movie_comments"] = get_movie_comment(movie_id=movie_id)

    # 电影信息
    data["movie_data"] = movie_search_by_id(movie_id)
    data["movie_5_cai"] = get_movie_5_cai(movie_id)
    # data["movie_data"] = movie_search_by_web(request.GET.get("id"))
    if not data['movie_data']:
        return render(request, 'tempate.html', {"tip": "电影信息无效，不存在有关信息！", "url": "/", "time": 3,
                                                "title": "错误页面", "data": data})
    cookie_uuid = request.COOKIES.get("uuid")
    if not cookie_uuid:
        cookie_uuid = uuid.uuid4().hex
        request.COOKIES["uuid"] = cookie_uuid
    response = render(request, 'movie.html', {"page": "movie.html", "data": data})
    response.set_cookie("uuid", cookie_uuid)
    delay_work.tag_thread_work("user_brow_tag", user_id=user_id, movie_id=movie_id)
    MovieBrows.objects.create(user_id=user_id, movie_id=movie_id, cookie_uuid=cookie_uuid)
    return response


# 忘记密码
def foget_password(request):
    data = page_nav(request)
    return render(request, 'userInfo.html', {"page": "forgetPwd.html", "data": data, "title": "忘记密码"})


# 用户中心
def user_info(request):
    data = page_nav(request)
    if isNotLogin(request):
        return render(request, 'tempate.html', {"tip": "请先登录！", "url": "/", "time": 3, "title": "错误页面",
                                                "data": data})
        # return JsonError("请先获取验证码！")
    user_id = request.session['user_id']
    userBase_rs = UsersBase.objects.filter(id=user_id)  # .values("user_passwd")
    if userBase_rs.exists():
        userBaseData = userBase_rs.first()
        usersDetailData = UsersDetail.objects.filter(user_id=userBaseData).first()
        data["userBaseData"] = userBaseData
        data["usersDetailData"] = usersDetailData
        data['user_hobbies'] = getHobbiesTag()
        return render(request, 'userInfo.html', {"page": "user_info_modify.html", "data": data, "title": "用户中心"})
    else:
        return render(request, 'tempate.html', {"tip": "用户不存在，请重新登陆！", "url": "/", "time": 3,
                                                "title": "错误页面", "data": data})


# 修改密码
def modify_password(request):
    data = page_nav(request)
    if isNotLogin(request):
        return render(request, 'tempate.html', {"tip": "请先登录！", "url": "/", "time": 3, "title": "错误页面",
                                                "data": data})
        # return JsonError("请先获取验证码！")
    user_id = request.session['user_id']
    user_rs = UsersBase.objects.filter(id=user_id)  # .values("user_passwd")
    if user_rs.exists():
        return render(request, 'userInfo.html', {"page": "user_password_modify.html", "data": data,
                                                 "title": "修改密码"})
    else:
        return render(request, 'tempate.html', {"tip": "用户不存在，请重新登陆！", "url": "/", "time": 3,
                                                "title": "错误页面", "data": data})


# 修改邮箱
def modify_email(request):
    data = page_nav(request)
    if isNotLogin(request):
        return render(request, 'tempate.html', {"tip": "请先登录！", "url": "/", "time": 3, "title": "错误页面",
                                                "data": data})
        # return JsonError("请先获取验证码！")
    user_id = request.session['user_id']
    user_rs = UsersBase.objects.filter(id=user_id)  # .values("user_passwd")
    if user_rs.exists():
        return render(request, 'userInfo.html', {"page": "user_email_modify.html", "data": data, "title": "修改邮箱"})
    else:
        return render(request, 'tempate.html', {"tip": "用户不存在，请重新登陆！", "url": "/", "time": 3,
                                                "title": "错误页面", "data": data})


# 用户收藏管理
def user_collection(request):
    data = page_nav(request)
    if isNotLogin(request):
        return render(request, 'tempate.html',
                      {"tip": "请先登录！", "url": "/", "time": 3, "title": "错误页面", "data": data})
        # return JsonError("请先获取验证码！")
    user_id = request.session['user_id']
    user_rs = UsersBase.objects.filter(id=user_id)  # .values("user_passwd")
    data["user_movie_like"] = get_user_like(user_id=user_id)
    if user_rs.exists():
        return render(request, 'userInfo.html',
                      {"page": "user_collection.html", "data": data, "title": "收藏管理"})
    else:
        return render(request, 'tempate.html',
                      {"tip": "用户不存在，请重新登陆！", "url": "/", "time": 3, "title": "错误页面", "data": data})


# 用户评论管理
def user_comment(request):
    data = page_nav(request)
    if isNotLogin(request):
        return render(request, 'tempate.html',
                      {"tip": "请先登录！", "url": "/", "time": 3, "title": "错误页面", "data": data})
        # return JsonError("请先获取验证码！")
    user_id = request.session['user_id']
    user_rs = UsersBase.objects.filter(id=user_id)  # .values("user_passwd")
    data["user_comment"] = get_user_comment(user_id=user_id)
    if user_rs.exists():
        return render(request, 'userInfo.html',
                      {"page": "user_comment.html", "data": data, "title": "评论管理"})
    else:
        return render(request, 'tempate.html',
                      {"tip": "用户不存在，请重新登陆！", "url": "/", "time": 3, "title": "错误页面", "data": data})


# 管理员验证
def check_admin_login(fn):
    def decorator(fn):
        @wraps(fn)
        def _wrapped_view(request, *args, **kwargs):
            data = page_nav(request)
            if isNotLogin(request):
                return render(request, 'tempate.html',
                              {"tip": "请先登录！", "url": "/", "time": 3, "title": "错误页面", "data": data})

            else:
                if request.session.get("user_role") == '2':
                    user = authenticate(username="Zero", password="1a2s3d4f")
                    login(request, user)
                    return fn(request, *args, **kwargs)
                else:
                    return render(request, 'tempate.html',
                                  {"tip": "无权限访问！", "url": "/", "time": 3, "title": "错误页面", "data": data})
                # 获取用户当前访问的url，并传递给/user/login/
                # next = request.get_full_path()
                # red = HttpResponseRedirect('/user/login/?next=' + next)
        # print(wrapper)
        return _wrapped_view
    return decorator


# 页面顶部信息获取
def page_nav(request):
    rs = dict()

    # data["nav_tag"] = nav_tag
    rs["movie_tag"] = movie_tag
    rs['movie_nav_tag'] = [{"tag": "", "data": []} for _ in range(4)]
    for i, tag in enumerate(default_tag):
        rs['movie_nav_tag'][i]["tag"] = tag
        rs['movie_nav_tag'][i]["data"] = get_index_tag_movie(tag, 2)

    user_id = request.session.get("user_id") if request.session.get("user_id") else 2
    if user_id != 2:
        # 获取用户对电影收藏信息
        rs["user_like"] = get_user_like(user_id=user_id, is_list=1)
        # 获取用户最近收藏的5部电影
        rs["user_5_like"] = get_user_movie_5_like(user_id)
        # 获取用户最近浏览的5部电影
        rs["user_5_brow"] = get_user_movie_5_brow(user_id)
        # 获取系统推荐的5部电影
        # rs["user_5_cai"] = get_movie_douban_top(1, 5)
        rs["user_5_cai"] = get_user_movie_5_cai(user_id)
    else:
        rs["user_like"] = []
        rs["user_5_like"] = []
        rs["user_5_brow"] = get_visiter_movie_5_brow(request.COOKIES.get("uuid"))
        rs["user_5_cai"] = []
    return rs
