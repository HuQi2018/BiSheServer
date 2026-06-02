import datetime

from django.db.models import Q
from rest_framework.views import APIView
from movie.models import MovieRatings, MovieLikes, \
    MovieComments, CollectMovieDB
from api import user_api, movie_api, api, delay_work
from api.response import JsonError, JsonResponse


Movie = movie_api.Movie()

emoution = Movie.emoution
movie_search_api = Movie.movie_search
get_user_movie_comment = Movie.get_user_movie_comment
get_user_search = Movie.get_user_search
get_user_movie_rating = Movie.get_user_movie_rating
get_user_movie_brow = Movie.get_user_movie_brow
get_user_like = Movie.get_user_like

isNotLogin = user_api.User().isNotLogin
get_ip = api.Api().get_ip

tag_thread_work = delay_work.tag_thread_work


# Create your views here.
def movie_search(request):
    return JsonResponse(movie_search_api(request))


# 电影评分
class MovieRating(APIView):
    def get(self, request, *args, **kwargs):
        if isNotLogin(request):
            return JsonError("请先登录！")
        try:
            rating = int(request.GET.get("rating"))
            movie_id = int(request.GET.get("movieId"))
            if not rating or not movie_id:
                raise Exception
        except:
            return JsonError("请确认请求参数无误！")
        user_id = request.session.get("user_id")
        rating_rs = MovieRatings.objects.filter(Q(user_id=user_id) & Q(movie_id=movie_id))
        if rating_rs.exists():
            tag_thread_work("user_rating_tag", user_id=user_id, movie_id=movie_id, old_rating=rating_rs.first().rating,
                            rating=rating, tag_sign="again")
            rating_rs.update(rating=rating, rating_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            if not CollectMovieDB.objects.filter(movie_id=movie_id).exists():
                return JsonError("电影信息不存在，评分失败！")
            tag_thread_work("user_rating_tag", user_id=user_id, movie_id=movie_id, rating=rating, tag_sign="init")
            MovieRatings.objects.create(user_id=user_id, movie_id=movie_id, rating=rating)
        return JsonResponse({"msg": "感谢您的评分！", "url": ""})

    def post(self, request, *args, **kwargs):
        return JsonError("不支持POST请求！")


# 电影收藏
class MovieLike(APIView):
    def get(self, request, *args, **kwargs):
        if isNotLogin(request):
            return JsonError("请先登录！")
        try:
            movie_id = int(request.GET.get("movieId"))
            if not movie_id:
                raise Exception
        except:
            return JsonError("请确认请求参数无误！")
        user_id = request.session.get("user_id")
        like_rs = MovieLikes.objects.filter(Q(user_id=user_id) & Q(movie_id=movie_id))
        if like_rs.exists():
            like_rs1 = like_rs.first()
            if like_rs1.status:
                like_rs.update(status=0)
                tag_thread_work("user_like_tag", user_id=user_id, movie_id=movie_id, tag_sign="cancel")
                msg = "取消收藏成功！"
            else:
                tag_thread_work("user_like_tag", user_id=user_id, movie_id=movie_id, tag_sign="like")
                like_rs.update(like_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), status=1)
                msg = "收藏成功！"
        else:
            if CollectMovieDB.objects.filter(movie_id=movie_id).exists():
                tag_thread_work("user_like_tag", user_id=user_id, movie_id=movie_id, tag_sign="init")
                MovieLikes.objects.create(user_id=user_id, movie_id=movie_id, status=1)
                msg = "收藏成功！"
            else:
                return JsonError("电影信息不存在，收藏失败！")
        return JsonResponse({"msg": msg, "url": ""})

    def post(self, request, *args, **kwargs):
        return JsonError("不支持POST请求！")


# 电影评论
class MovieComment(APIView):
    def get(self, request, *args, **kwargs):
        return JsonError("不支持GET请求！")

    def post(self, request, *args, **kwargs):
        if isNotLogin(request):
            return JsonError("请先登录！")

        title = request.POST.get("title")
        user_id = request.session.get("user_id")
        user_uname = request.session.get("user_uname")
        movie_name = request.POST.get("movie_title")
        movie_id = request.POST.get("movie_id")
        content_text = request.POST.get("content_text")
        ip = get_ip(request)
        if movie_id and content_text and title:
            emotion = emoution(content_text)
            if not CollectMovieDB.objects.filter(movie_id=movie_id).exists():
                return JsonError("电影信息不存在，评论失败！")
            tag_thread_work("user_comment_tag", user_id=user_id, movie_id=movie_id, emotion=emotion, tag_sign="add")
            movie_comment = MovieComments.objects.create(user_id=user_id, movie_id=movie_id, userName=user_uname,
                                                         title=title, movieName=movie_name, content=content_text,
                                                         emotion=emotion, ip=ip)
        else:
            return JsonError("评论失败，标题和内容不能为空！")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment = {"userName": user_uname, "user": str(user_id), "comment_time": now, "title": title,
                   "content": content_text, "id": movie_comment.id}
        return JsonResponse({"msg": "评论成功！", "url": "", "comment": comment})


# 删除电影评论
class MovieCommentDelete(APIView):
    def get(self, request, *args, **kwargs):
        if isNotLogin(request):
            return JsonError("请先登录！")
        try:
            comment_id = int(request.GET.get("comment_id"))
            if not comment_id:
                raise Exception
        except:
            return JsonError("请确认请求参数无误！")
        user_id = request.session.get("user_id")
        comment_rs = MovieComments.objects.filter(Q(user_id=user_id) & Q(id=comment_id))
        if comment_rs.exists():
            tag_thread_work("user_comment_tag", user_id=user_id, movie_id=comment_rs.first().movie_id,
                            emotion=comment_rs.first().emotion, tag_sign="delete")
            comment_rs.update(status=0)
            return JsonResponse({"msg": "评论删除成功！", "url": ""})
        else:
            return JsonError("您没有权限删除该评论！")

    def post(self, request, *args, **kwargs):
        return JsonError("不支持POST请求！")

# def get_roles_page(self,_page,_limit):
#   _roles = SysRole.objects.all()[(int(_page)-1)*int(_limit):int(_page)*int(_limit)]
#   _count = SysRole.objects.all().count()
#   _dict_roles = tools.queryset_to_json(_roles)
#   _data_page_json = {}
#   _data_page_json['Rows']=_dict_roles
#   _data_page_json['Total']=_count
#   return json.dumps(_data_page_json,ensure_ascii=False)


# def recommendForUser(request):
#     """
#         向用户进行top5推荐
#             如果用户已经登陆， 从default和top中进行混合随机推荐
#             如果用户没有登陆， 从default中进行推荐
#     :param request:
#     :return:
#     """
#     user = request.user
#     user_recommend_movies = None
#     default_recommend_movies = list(map(lambda x: x.movie
#                                         , list(Default5Recommend.objects.filter(redate=datetime.date.today()))))
#     if user.is_authenticated:
#         # 如果用户已经登陆
#         user_recommend_movies = list(map(lambda x: x.movie
#                                          , list(Top5Recommend.objects.filter(user_id__in=[user.id]))))
#         # defautl和recommend随机选取5个， 同时避免了recommend不足5个的情况
#         user_recommend_movies = user_recommend_movies + default_recommend_movies
#         user_recommend_movies = random.sample(user_recommend_movies, 5)
#     else:
#         # 如果用户没有登陆
#         user_recommend_movies = default_recommend_movies
#     return user_recommend_movies
#
#
# class IndexView(View):
#     def get(self, request):
#         # 用户登陆则推荐电影， 否则推荐默认电影（固定五部）
#         # return render(request, 'index.html', {})
#         user = request.user
#         # de_recommend = list(DefaultPop5Result.objects.filter(redate=datetime.date.today())\
#         #     .values('movie__moviename', 'movie__averating', 'movie__description', 'movie__picture'))
#         # de_recommend = list(map(lambda x: x.movie
#         # , list(Default5Recommend.objects.filter(redate=datetime.date.today()))))
#         # user_recommend_movie = None
#         # if user.is_authenticated:
#         #     # recommend_movie = list(Top5Recomm.objects.filter(user_id__in=[user.id])\
#         #     #     .values('movie__moviename', 'movie__averating', 'movie__description', 'movie__picture'))
#         #     user_recommend_movie = list(map(lambda x: x.movie
#         #                            , list(Top5Recommend.objects.filter(user_id__in=[user.id]))))
#         #     # defautl和recommend随机选取5个， 同时避免了recommend不足5个的情况
#         #     user_recommend_movie = user_recommend_movie + de_recommend
#         #     user_recommend_movie = random.sample(user_recommend_movie, 5)
#         # else:
#         #     user_recommend_movie = de_recommend
#         user_recommend_movie = recommendForUser(request=request)
#
#         all_movieinfo = MovieInfo.objects.all().order_by('-releasedate')
#         movieinfo = all_movieinfo[1:9]
#         movietitle = all_movieinfo[1]
#         movielatest = all_movieinfo[9:18]
#         return render(request, 'index.html', {
#             "moiveinfo": movieinfo,
#             "movietitle": movietitle,
#             "movielatest": movielatest,
#             "user_recommend_movie": user_recommend_movie,
#         })
#
# class ContentView(View):
#     def get(self, request, movie_id):
#         # # all_movieinfo = MovieInfo.objects.get(id=int(movie_id))
#         # # all_movie = all_movieinfo.objects.all();
#         # # print(all_movie.name)
#         # movieinfo = MovieInfo.objects.get(id=movie_id)
#         #
#         # similar_movies_id = MovieSimilar.objects.all()
#         movieinfo = MovieInfo.objects.get(id=movie_id)
#         # 对用户进行的个性化推荐
#         user_recommend_movies = recommendForUser(request)
#         # 相似电影
#         similar_movies_ids = MovieSimilar.objects.filter(item1=movie_id).order_by('-similar')[:10]
#         # similar_movies = list(map(lambda x: MovieInfo.objects.get(x.movie_id), similar_movies))
#         similar_movies = list(map(lambda x: MovieInfo.objects.get(id=x.item2), similar_movies_ids))
#         all_comments = Review.objects.all()
#         # all_movieinfo = MovieInfo.objects.all()
#         # movielaster = all_movieinfo[0:2]
#         return render(request, 'content.html', {"movieinfo": movieinfo,
#                                                 # "movielaster": movielaster,
#                                                 "similar_movies": similar_movies,
#                                                 "recommend_movies": user_recommend_movies,
#                                                 "all_comments":all_comments})
