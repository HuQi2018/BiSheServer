# from django.shortcuts import render
import random

from django.http import HttpResponse

from api import movie_api
from api.response import JsonError, JsonResponse
from movie.models import CollectMovieDB, MovieTagDB
from user.models import UsersBase, UserTag
from django.db.models import Q

from rest_framework.views import APIView


# Create your views here.
def user_login(request):
    # 初始化
    response = ""
    response1 = ""

    # user_count = request
    # user_rs = UsersBase.objects.filter(Q(user_name=user_count) | Q(user_phone=user_count) | Q(user_mail=user_count))\
    #     .first().values("user_passwd")
    # if user_rs.exists():
    #     return render("index.html")
    # return render("index.html")

# def createAdmin(request, *args, **kwargs):
#     user = User.objects.create_user(username='admin', password='123456', email='995269681@qq.com')
#     user.save()  # 调用该方法保存数据
#     return HttpResponse("<p>管理员添加成功！</p>")


def movie_collections(request):
    movie_obj = CollectMovieDB.objects.aggregate([
        {"$match": {'movie_id': int(10736563)}},
        {'$sample': {'size': int(20)}},
        {"$project": {"rating": 1}},
        {"$sort": {"movie_id": -1}}])
    print(movie_obj)
    return HttpResponse(movie_obj)


class logout(APIView):
    def get(self, request, *args, **kwargs):
        if request.session['is_login']:  # 如果已登录则注销
            request.session.flush()
            # return HttpResponseRedirect('')  #跳转到index界面
            return HttpResponse("注销成功！")
        else:
            HttpResponse("您还未登陆！")

    def post(self, request, *args, **kwargs):
        return JsonError("不支持POST请求！")


class TryView(APIView):
    def get(self, request, *args, **kwargs):
        user_count = "zero12"
        user_rs = UsersBase.objects.filter(Q(user_name=user_count) | Q(user_phone=user_count) | Q(
            user_mail=user_count))  # .values("user_passwd")
        if user_rs.exists():
            print("存在！")
        # conn = redis.Redis(connection_pool=POOL)
        # conn.set("key", "data")
        # conn.expire("key", 60 * 60 * 24)
        # data = conn.get("key")
        return JsonResponse("GET请求成功！Redis数据为：")

    def post(self, request, *args, **kwargs):
        return JsonResponse("POST请求成功！"+request.POST)


# 用户注册第一步
class user_register1(APIView):
    def get(self, request, *args, **kwargs):
        return JsonError("不支持Get请求！")

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            print('Key: %s' % (key))
            print('Value %s' % (value))
        return JsonResponse("POST请求成功！请求的数据data为：")


# 返回对应类别的movie_id
def get_movie_tag_li(tag_name):
    return list(MovieTagDB.objects.filter(Q(tag_type='genre') & Q(tag_name=tag_name)).values_list("movie_id_id",flat=True))


# 添加交集
def add_more(get_movie_tag_li0, get_movie_tag_li1):
    movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li1))
    if len(movie_id_rs) > 5:
        return movie_id_rs
    else:
        return get_movie_tag_li0


# 获取最大交集的5个tag的movie_id
def get_5_tag_movie_id(tag_name):
    movie_id_rs = list()
    if len(tag_name) == 1:
        movie_id_rs = get_movie_tag_li(tag_name[0])

    if len(tag_name) == 2:
        get_movie_tag_li0 = get_movie_tag_li(tag_name[0])
        get_movie_tag_li1 = get_movie_tag_li(tag_name[1])
        movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li1))
        if len(movie_id_rs) < 5:  # 如果第一种类型与第二种类型不存在同时存在的电影就直接取第一种类型的结果
            movie_id_rs = get_movie_tag_li0

    if len(tag_name) == 3:
        get_movie_tag_li0 = get_movie_tag_li(tag_name[0])
        get_movie_tag_li1 = get_movie_tag_li(tag_name[1])
        movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li1))
        if len(movie_id_rs) < 5:  # 如果第一种类型与第二种类型不存在同时存在的电影就进行与第三个类型匹配
            get_movie_tag_li2 = get_movie_tag_li(tag_name[2])
            movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li2))
        if len(movie_id_rs) > 300:  # 如果第一种与第二种类型存在的结果较多则再与第三种类型交集
            get_movie_tag_li2 = get_movie_tag_li(tag_name[2])
            movie_id_rs = add_more(movie_id_rs, get_movie_tag_li2)
        if len(movie_id_rs) < 5:  # 如果第一种类型与第二种类型不存在同时存在的电影就直接取第一种类型的结果
            movie_id_rs = get_movie_tag_li0

    if len(tag_name) == 4:
        get_movie_tag_li0 = get_movie_tag_li(tag_name[0])
        get_movie_tag_li1 = get_movie_tag_li(tag_name[1])
        movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li1))
        if len(movie_id_rs) < 5:  # 如果第一种类型与第二种类型不存在同时存在的电影就进行与第三个类型匹配
            get_movie_tag_li2 = get_movie_tag_li(tag_name[2])
            movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li2))
        if len(movie_id_rs) < 5:  # 如果第一种类型与第三种类型不存在同时存在的电影就进行与第四个类型匹配
            get_movie_tag_li3 = get_movie_tag_li(tag_name[3])
            movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li3))
        if len(movie_id_rs) > 300:  # 如果第一种与第二种类型存在的结果较多则再与第三种类型交集
            get_movie_tag_li2 = get_movie_tag_li(tag_name[2])
            movie_id_rs = add_more(movie_id_rs, get_movie_tag_li2)
        if len(movie_id_rs) > 300:  # 如果第一种、第二种与第三种类型存在的结果较多则再与第四种类型交集
            get_movie_tag_li3 = get_movie_tag_li(tag_name[3])
            movie_id_rs = add_more(movie_id_rs, get_movie_tag_li3)
        if len(movie_id_rs) < 5:  # 如果第一种类型与第四种类型不存在同时存在的电影就直接取第一种类型的结果
            movie_id_rs = get_movie_tag_li0
    movie_id_rs = random.sample(movie_id_rs, 5)
    return movie_id_rs


def try_get(request):
    # user_id = request.session.get("user_id") if request.session.get("user_id") else 2
    # movie_id = request.GET.get("id")
    # rs = movie_api.Movie().get_user_like(user_id)
    # print(rs)
    tag_name = UserTag.objects.filter(Q(tag_type='info_movie_type') & Q(user_id=1))\
        .order_by("-tag_weight").all().values_list("tag_name", flat=True)
    tag_name = list(tag_name)[:4]
    movie_id_rs = get_5_tag_movie_id(tag_name)

    return JsonResponse("请求成功！请求的数据data为：{}".format(movie_id_rs))


def user_modify(request):
    books = UsersBase.objects.filter(pk__in=[7,8]).update(price=888)
    # form = LoginForm(request.POST)
    # if form.is_valid():
    # if request.path == '/test/':
    #     return redirect('http://www.baidu.com')
    # return HttpResponseRedirect('/login/')
    #  return render() redirect('/')

    # username = request.session.get('username', '')
    # if not username:
    #     return HttpResponseRedirect('/login/')

    # if request.session.get('has_commented', False):
    #     return HttpResponse("You've already commented.")
    #     c = comments.Comment(comment=new_comment)
    #     c.save()
    #     request.session['has_commented'] = True
    # return HttpResponse('Thanks for your comment!')
    return HttpResponse(books)
