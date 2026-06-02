import datetime
import random
from functools import reduce

import requests
from bs4 import BeautifulSoup
from django.db.models import Q
from snownlp import SnowNLP

from api import delay_work
from user.models import UserTag, UserMovieRecommend
from .api import Api
from api.model_json import queryset_to_json
from movie.models import CollectMovieTypeDB, CollectMovieDB, MovieLikes, MovieRatings, MovieComments, MovieSearchs, \
    MovieBrows, MovieRatingDB, MoviePubdateDB, MovieTagDB
set_readis = Api().set_readis
get_readis = Api().get_readis


class Movie:

    def __init__(self):
        pass

    # 获取电影标签
    @staticmethod
    def get_movie_tag():
        movie_tag_rs = CollectMovieTypeDB.objects.all()
        return movie_tag_rs

    # 获取电影标签的JSON数据集
    @staticmethod
    def get_movie_tag_json(self):
        movie_tag_rs = queryset_to_json(self.get_movie_tag())
        return movie_tag_rs

    # 电影搜索页面的api
    def movie_search(self, request):
        key = request.GET.get("s") if request.GET.get("s") else ""
        movie_type = request.GET.get("type") if request.GET.get("type") else ""
        page = request.GET.get("page") if request.GET.get("page") else 1
        limit = request.GET.get("limit") if request.GET.get("limit") else 20
        # 2标识固定为访客
        user_id = request.session.get("user_id") if request.session.get("user_id") else 2
        cookie_uuid = request.COOKIES.get("uuid")
        # allow_type = ['title', 'year', 'tags', 'genres', 'countries', 'languages', 'all']

        if movie_type == 'new':
            key = "最新电影"
            movie_obj = MoviePubdateDB.objects.count()
        elif movie_type == 'top':
            key = "高分电影"
            movie_obj = MovieRatingDB.objects.count()
        else:
            movie_obj = CollectMovieDB.objects.order_by("-year", "-pubdate", "-ratings_count")

        _data_page_json = get_readis(str(movie_type)+"_"+str(key)+"_"+str(page)+"_"+str(limit))

        if key:
            delay_work.tag_thread_work("user_search_tag", user_id=user_id, search_key=key, movie_type=movie_type)
            MovieSearchs.objects.create(user_id=user_id, type=movie_type, limit=limit, page=page, content=key,
                                        cookie_uuid=cookie_uuid)

        if _data_page_json:
            return _data_page_json

        _count = 0
        if movie_type == 'new':
            movie_search_rs = self.get_movie_douban_new(page, limit)
            _count = movie_obj
        elif movie_type == 'top':
            movie_search_rs = self.get_movie_douban_top(page, limit)
            _count = movie_obj
        elif movie_type == 'title':
            movie_search_rs = movie_obj.filter(Q(title__contains=key) | Q(original_title__contains=key))
        elif movie_type == 'year':
            movie_search_rs = movie_obj.filter(year=key)
        elif movie_type == 'tag':
            movie_search_rs = movie_obj.filter(tags__contains=key)
        elif movie_type == 'genres':
            movie_search_rs = movie_obj.filter(genres__contains=key)
        elif movie_type == 'countries':
            movie_search_rs = movie_obj.filter(countries__contains=key)
        elif movie_type == 'languages':
            movie_search_rs = movie_obj.filter(languages__contains=key)
        elif movie_type == 'all':
            movie_search_rs = movie_obj.filter(
                Q(title__contains=key) | Q(original_title__contains=key) | Q(year__contains=key)
                | Q(tags__contains=key) | Q(genres__contains=key) | Q(countries__contains=key) | Q(
                    languages__contains=key))
        else:
            return {'Rows': [], 'Total': 0, 'Page': 0, 'NextPage': 0}

        # print(movie_search_rs[0])
        if movie_type != 'new' and movie_type != 'top':
            movie_search_rs = movie_search_rs.all()
            _count = len(movie_search_rs)
            # _count = movie_search_rs.count()
            movie_search_rs = movie_search_rs[(int(page) - 1) * int(limit):int(page) * int(limit)]
            # movie_search_rs_json = serializers.serialize('json', movie_search_rs)
            movie_search_rs_json = queryset_to_json(movie_search_rs)
        else:
            movie_search_rs_json = movie_search_rs
        # movie_search_rs_json = convert_obj_to_json(movie_search_rs)
        # movie_search_rs_json = movie_search_rs.values("movie_id","images","rating","title","actor","year","pubdate")
        _data_page_json = dict()
        _data_page_json['Rows'] = movie_search_rs_json
        _data_page_json['Total'] = _count
        _data_page_json['Page'] = page
        _data_page_json['NextPage'] = int(page) + 1
        _data_page_json['Type'] = movie_type
        _data_page_json['Key'] = key
        _data_page_json['Limit'] = limit

        set_readis(str(movie_type)+"_"+str(key)+"_"+str(page)+"_"+str(limit), _data_page_json)

        return _data_page_json

    # 电影详情信息获取
    @staticmethod
    def movie_search_by_id(movie_id):
        if not movie_id:
            return {}

        _data_page_json = get_readis("movie_id_"+str(movie_id))
        if _data_page_json:
            return _data_page_json

        movie_search_rs = CollectMovieDB.objects.filter(movie_id=movie_id).all()
        movie_search_rs_json = queryset_to_json(movie_search_rs)
        # if type(movie_search_rs_json) == list:
        #     movie_search_rs_json = movie_search_rs_json[0]
        movie_search_rs_json = movie_search_rs_json[0]

        set_readis("movie_id_"+str(movie_id), movie_search_rs_json)

        return movie_search_rs_json

    # 评论情感api
    # 好评：76.58088675002497
    # 差评：18.494829160412728
    @staticmethod
    def emoution(sentece):
        sent = SnowNLP(sentece)
        predict = sent.sentiments * 100
        return predict

    # 获取用户收藏的指定电影
    @staticmethod
    def get_user_movie_like(user_id, movie_id, is_list=0):

        user_movie_like_rs = MovieLikes.objects.order_by("-like_time").filter(Q(user_id=user_id) &
                                                                              Q(movie_id=movie_id) & Q(status=1)).all()
        if is_list:  # 若为1，则返回movie_id的结果集
            user_movie_like_rs_json = list(user_movie_like_rs.values_list("movie__movie_id", flat=True))
        else:
            user_movie_like_rs_json = queryset_to_json(user_movie_like_rs)
        return user_movie_like_rs_json

    # 获取用户最近收藏的5部电影
    def get_user_movie_5_like(self, user_id):

        user_movie_like_rs = MovieLikes.objects.order_by("-like_time").filter(Q(user_id=user_id) & Q(status=1)).all()
        user_movie_5_like_rs_list = list(user_movie_like_rs.values_list("movie__movie_id", flat=True))[:5]
        # movie_search_rs = CollectMovieDB.objects.filter(movie_id__in=user_movie_5_like_rs_list).all()
        # user_movie_5_like_rs_json = queryset_to_json(movie_search_rs)
        user_movie_5_like_rs = []
        for movie_id in user_movie_5_like_rs_list:
            user_movie_5_like_rs.append(self.movie_search_by_id(movie_id))
        # movie_search_rs_json = serializers.serialize('json', movie_search_rs)
        user_movie_5_like_rs_json = user_movie_5_like_rs
        return user_movie_5_like_rs_json

    # 获取用户收藏的所有电影
    @staticmethod
    def get_user_like(user_id, is_list=0):

        user_like_rs = MovieLikes.objects.order_by("-like_time").filter(Q(user_id=user_id) & Q(status=1)).all()
        user_like_rs_json = list(user_like_rs.values_list("movie__movie_id", flat=True))
        if not is_list:  # 若为0，则返回所有电影信息，否则返回movie_id的结果集
            movie_like_rs = CollectMovieDB.objects.filter(movie_id__in=user_like_rs_json).all()
            user_like_rs_json = queryset_to_json(movie_like_rs)
        return user_like_rs_json

    # 获取用户对某一部电影的评分
    @staticmethod
    def get_user_movie_rating(user_id, movie_id, is_list=0):

        user_movie_rating_rs = MovieRatings.objects.order_by("-rating_time").filter(Q(user_id=user_id) &
                                                                                    Q(movie_id=movie_id)).all()
        if is_list:  # 若为1，则返回movie_id的结果集
            user_movie_rating_rs_json = list(user_movie_rating_rs.values_list("movie_id", "rating"))
        else:
            user_movie_rating_rs_json = queryset_to_json(user_movie_rating_rs)
        return user_movie_rating_rs_json

    # 获取某一部电影的所有评论
    @staticmethod
    def get_movie_comment(movie_id, is_list=0):

        movie_comment_rs = MovieComments.objects.order_by("comment_time").filter(Q(movie_id=movie_id) &
                                                                                 Q(status=1)).all()
        if is_list:  # 若为1，则返回id的结果集
            movie_comment_rs_json = list(movie_comment_rs.values_list("id", flat=True))
        else:
            movie_comment_rs_json = queryset_to_json(movie_comment_rs)
        return movie_comment_rs_json

    # 获取用户的所有评论
    @staticmethod
    def get_user_comment(user_id, is_list=0):

        movie_comment_rs = MovieComments.objects.order_by("-comment_time").filter(Q(user_id=user_id) &
                                                                                  Q(status=1)).all()
        if is_list:  # 若为1，则返回id的结果集
            movie_comment_rs_json = list(movie_comment_rs.values_list("id", flat=True))
        else:
            movie_comment_rs_json = queryset_to_json(movie_comment_rs)
        return movie_comment_rs_json

    # 获取用户对某一部电影的评论
    @staticmethod
    def get_user_movie_comment(user_id, movie_id, is_list=0):

        user_movie_comment_rs = MovieComments.objects.order_by("comment_time").filter(Q(user_id=user_id) &
                                                                                      Q(movie_id=movie_id) &
                                                                                      Q(status=1)).all()
        if is_list:  # 若为1，则返回id的结果集
            user_movie_comment_rs_json = list(user_movie_comment_rs.values_list("id", flat=True))
        else:
            user_movie_comment_rs_json = queryset_to_json(user_movie_comment_rs)
        return user_movie_comment_rs_json

    #  获取用户的所有搜索结果
    @staticmethod
    def get_user_search(user_id):

        user_movie_search_rs = MovieSearchs.objects.order_by("-search_time").filter(user_id=user_id).all()
        user_movie_search_rs_json = queryset_to_json(user_movie_search_rs)
        return user_movie_search_rs_json

    # 获取用户的所有浏览记录
    @staticmethod
    def get_user_movie_brow(user_id):

        user_movie_brow_rs = MovieBrows.objects.order_by("-brow_time").filter(user_id=user_id).all()
        user_movie_brow_rs_json = queryset_to_json(user_movie_brow_rs)
        return user_movie_brow_rs_json

    # 获取用户最近浏览的5部电影
    def get_user_movie_5_brow(self, user_id):

        user_movie_brow_rs = MovieBrows.objects.order_by("-brow_time").filter(user_id=user_id).all()
        user_movie_5_brow_rs_list = list(user_movie_brow_rs.values_list("movie_id", flat=True))
        # 去重
        user_movie_5_brow_rs_list = reduce(lambda x, y: x if y in x else x + [y], [[], ] +
                                           user_movie_5_brow_rs_list)[:5]
        # movie_search_rs = CollectMovieDB.objects.filter(movie_id__in=user_movie_5_brow_rs_list[:5]).all()
        # movie_search_rs_json = queryset_to_json(movie_search_rs)
        user_movie_5_brow_rs = []
        for movie_id in user_movie_5_brow_rs_list:
            user_movie_5_brow_rs.append(self.movie_search_by_id(movie_id))
        # movie_search_rs_json = serializers.serialize('json', user_movie_5_brow_rs)
        user_movie_5_like_rs_json = user_movie_5_brow_rs
        return user_movie_5_like_rs_json

    # 获取访客最近浏览的5部电影
    def get_visiter_movie_5_brow(self, cookie_uuid):
        if not cookie_uuid:
            return []
        visiter_movie_brow_rs = MovieBrows.objects.order_by("-brow_time").filter(cookie_uuid=cookie_uuid).all()
        visiter_movie_5_brow_rs_list = list(visiter_movie_brow_rs.values_list("movie_id", flat=True))
        # 去重
        visiter_movie_5_brow_rs_list = reduce(lambda x, y: x if y in x else x + [y], [[], ] +
                                              visiter_movie_5_brow_rs_list)[:5]
        # movie_search_rs = CollectMovieDB.objects.filter(movie_id__in=user_movie_5_brow_rs_list[:5]).all()
        # movie_search_rs_json = queryset_to_json(movie_search_rs)
        visiter_movie_5_brow_rs = []
        for movie_id in visiter_movie_5_brow_rs_list:
            visiter_movie_5_brow_rs.append(self.movie_search_by_id(movie_id))
        # movie_search_rs_json = serializers.serialize('json', user_movie_5_brow_rs)
        visiter_movie_5_like_rs_json = visiter_movie_5_brow_rs
        return visiter_movie_5_like_rs_json

    # 获取最新的5部电影
    def get_movie_douban_new(self, page=1, num=5):

        movie_douban_new_rs_json = get_readis("movie_new"+"_"+str(page)+"_"+str(num))
        if movie_douban_new_rs_json:
            return movie_douban_new_rs_json

        movie_douban_new_rs = MoviePubdateDB.objects.order_by("-pubdate").filter(pubdate__lte=datetime.datetime.now()
                                                                                 .strftime('%Y-%m-%d')).all()
        movie_douban_new_rs_list = list(movie_douban_new_rs.values_list("movie_id", flat=True)
                                        [(int(page) - 1) * int(num):int(page) * int(num)])
        # 去重
        # movie_douban_new_rs_list = reduce(lambda x, y: x if y in x else x + [y], [[], ] + movie_douban_new_rs_list)
        # movie_search_rs = CollectMovieDB.objects.filter(movie_id__in=user_movie_5_brow_rs_list[:5]).all()
        # movie_search_rs_json = queryset_to_json(movie_search_rs)
        movie_douban_new_rs = []
        for movie_id in movie_douban_new_rs_list:
            movie_douban_new_rs.append(self.movie_search_by_id(movie_id))
        # movie_search_rs_json = serializers.serialize('json', user_movie_5_brow_rs)
        movie_douban_new_rs_json = movie_douban_new_rs

        set_readis("movie_new"+"_"+str(page)+"_"+str(num), movie_douban_new_rs_json)

        return movie_douban_new_rs_json

    # 获取指定标签电影
    @staticmethod
    def get_tag_movie(tag_type, tag_name):
        # tag_movie_rs = MovieTagDB.objects.filter(tag_type=tag_type, tag_name=tag_name)\
        #     .order_by("-moviepubdatedb__pubdate", "-movieratingdb__rating").all()
        tag_movie_rs = MovieTagDB.objects.filter(tag_type=tag_type, tag_name=tag_name).all()
        tag_movie_rs_list = list(tag_movie_rs.values_list("movie_id", flat=True))
        return tag_movie_rs_list

    # 获取根据类别获取主页显示推荐的电影
    def get_index_tag_movie(self, tag_name, user_id, num=5):

        index_tag_movie_rs_json = get_readis("index_movie_tag"+"_"+str(tag_name)+"_"+str(user_id)+"_"+str(num))
        if index_tag_movie_rs_json:
            return index_tag_movie_rs_json

        index_tag_movie_rs_list = self.get_tag_movie('tag', tag_name)
        # 去重
        # index_tag_movie_rs_list = reduce(lambda x, y: x if y in x else x + [y], [[], ] +
        #                                  index_tag_movie_rs_list)[:num]
        # index_tag_movie_rs = CollectMovieDB.objects.order_by("-year", "-movieratingdb__rating",
        #                                                      "-moviepubdatedb__pubdate")\
        #     .filter(movie_id__in=index_tag_movie_rs_list).all()
        # index_tag_movie_rs_json = queryset_to_json(index_tag_movie_rs)
        if len(index_tag_movie_rs_list) > 4:
            index_tag_movie_rs_list = random.sample(index_tag_movie_rs_list[:300], 5)
        index_tag_movie_rs = []
        for movie_id in index_tag_movie_rs_list:
            index_tag_movie_rs.append(self.movie_search_by_id(movie_id))
        # movie_search_rs_json = serializers.serialize('json', user_movie_5_brow_rs)
        index_tag_movie_rs_json = index_tag_movie_rs
        # 设置10分钟缓存不变
        set_readis("index_movie_tag"+"_"+str(tag_name)+"_"+str(user_id)+"_"+str(num), index_tag_movie_rs_json,
                   set_time=60 * 10)

        return index_tag_movie_rs_json

    # 获取豆瓣高分10部电影
    def get_movie_douban_top(self, page=1, num=10):

        movie_douban_top_rs_json = get_readis("movie_top"+"_"+str(page)+"_"+str(num))
        if movie_douban_top_rs_json:
            return movie_douban_top_rs_json

        movie_douban_top_rs = MovieRatingDB.objects.order_by("-rating").all()
        movie_douban_top_rs_list = list(movie_douban_top_rs.values_list("movie_id", flat=True)
                                        [(int(page) - 1) * int(num):int(page) * int(num)])
        # 去重
        # movie_douban_top_rs_list = reduce(lambda x, y: x if y in x else x + [y], [[], ] +
        #                                   movie_douban_top_rs_list)[:num]
        # movie_search_rs = CollectMovieDB.objects.filter(movie_id__in=user_movie_5_brow_rs_list[:5]).all()
        # movie_search_rs_json = queryset_to_json(movie_search_rs)
        movie_douban_top_rs = []
        for movie_id in movie_douban_top_rs_list:
            movie_douban_top_rs.append(self.movie_search_by_id(movie_id))
        # movie_search_rs_json = serializers.serialize('json', user_movie_5_brow_rs)
        movie_douban_top_rs_json = movie_douban_top_rs

        set_readis("movie_top"+"_"+str(page)+"_"+str(num), movie_douban_top_rs_json)

        return movie_douban_top_rs_json

    # 爬取豆瓣的信息
    @staticmethod
    def movie_search_by_web(movie_id):
        if not movie_id:
            return {}

        url = 'https://movie.douban.com/subject/' + str(movie_id) + '/'
        # https://movie.douban.com/j/subject_abstract?subject_id=34603816
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/62.0.3202.94 Safari/537.36'}
            html = requests.get(url, headers=headers, timeout=10)
        except Exception as e:
            print(e)
            return {"status": 0, "message": "获取失败！' + str(e) + '", "data": {}}
            # break
        if html.status_code == 404:
            return {"status": 0, "message": "获取失败，不存在有关信息！", "data": {}}
        data = {}
        soup = BeautifulSoup(html.text.encode("utf-8"), features='html.parser')
        soup = soup.find(name='div', attrs={'id': 'wrapper'})
        # print(soup.h1.span.string)
        data['title'] = soup.h1.span.string  # 标题
        article = soup.find(name='div', attrs={'class': 'subjectwrap'})
        data['article'] = str(article)  # 信息
        summ = soup.find(name='div', attrs={'id': 'link-report'})
        summary = summ.find(name='span', attrs={'class': 'short'})
        if summary:
            summary = str(summary)
        else:
            summary = str(summ)
        data['summary'] = str(summary)  # 简述内容简介
        all_summary = soup.find(name='span', attrs={'class': 'all hidden'})
        data['allSummary'] = str(all_summary)  # 内容简介
        if type == 'book':
            intro = soup.find(text='作者简介')
            if intro:
                try:
                    data['info'] = str(intro.parent.parent.next_sibling.next_sibling.div.div.text)  # 作者简介
                except Exception as ex:
                    print(ex)
                    data['info'] = str(intro.parent.parent.next_sibling.next_sibling.span.div.text)  # 作者简介
                    pass
            # print(data['info'])
            tag = soup.find(name='div', attrs={'id': 'db-tags-section'})
            tags = [td.a.string for td in tag.div.find_all('span')]
        else:
            tag = soup.find(name='div', attrs={'class': 'tags-body'})
            tags = [td.string for td in tag.find_all('a')]
        data['tags'] = tags  # 标签

        # data = json.dumps(data)
        return {"status": 1, "message": "获取成功！", "data": str(data), "url": str(url)}

    # 返回对应类别的movie_id
    @staticmethod
    def get_movie_tag_li(tag_name):
        return list(
            MovieTagDB.objects.filter(Q(tag_type='genre') & Q(tag_name=tag_name)).values_list("movie_id_id", flat=True))

    # 添加交集
    @staticmethod
    def add_more_tag(get_movie_tag_li0, get_movie_tag_li1):
        movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li1))
        if len(movie_id_rs) > 5:
            return movie_id_rs
        else:
            return get_movie_tag_li0

    # 获取最大交集的5个tag的movie_id， 最大只能有4个类型传入
    def get_5_tag_movie_id(self, tag_name):
        if not tag_name:
            return []
        tag_name = tag_name[:4]
        # print(tag_name)
        movie_id_rs = list()
        if len(tag_name) == 1:
            movie_id_rs = self.get_movie_tag_li(tag_name[0])

        if len(tag_name) == 2:
            get_movie_tag_li0 = self.get_movie_tag_li(tag_name[0])
            get_movie_tag_li1 = self.get_movie_tag_li(tag_name[1])
            movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li1))
            if len(movie_id_rs) < 5:  # 如果第一种类型与第二种类型不存在同时存在的电影就直接取第一种类型的结果
                movie_id_rs = get_movie_tag_li0

        if len(tag_name) == 3:
            get_movie_tag_li0 = self.get_movie_tag_li(tag_name[0])
            get_movie_tag_li1 = self.get_movie_tag_li(tag_name[1])
            movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li1))
            if len(movie_id_rs) < 5:  # 如果第一种类型与第二种类型不存在同时存在的电影就进行与第三个类型匹配
                get_movie_tag_li2 = self.get_movie_tag_li(tag_name[2])
                movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li2))
            if len(movie_id_rs) > 300:  # 如果第一种与第二种类型存在的结果较多则再与第三种类型交集
                get_movie_tag_li2 = self.get_movie_tag_li(tag_name[2])
                movie_id_rs = self.add_more_tag(movie_id_rs, get_movie_tag_li2)
            if len(movie_id_rs) < 5:  # 如果第一种类型与第二种类型不存在同时存在的电影就直接取第一种类型的结果
                movie_id_rs = get_movie_tag_li0

        if len(tag_name) == 4:
            get_movie_tag_li0 = self.get_movie_tag_li(tag_name[0])
            get_movie_tag_li1 = self.get_movie_tag_li(tag_name[1])
            movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li1))
            if len(movie_id_rs) < 5:  # 如果第一种类型与第二种类型不存在同时存在的电影就进行与第三个类型匹配
                get_movie_tag_li2 = self.get_movie_tag_li(tag_name[2])
                movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li2))
            if len(movie_id_rs) < 5:  # 如果第一种类型与第三种类型不存在同时存在的电影就进行与第四个类型匹配
                get_movie_tag_li3 = self.get_movie_tag_li(tag_name[3])
                movie_id_rs = list(set(get_movie_tag_li0).intersection(get_movie_tag_li3))
            if len(movie_id_rs) > 300:  # 如果第一种与第二种类型存在的结果较多则再与第三种类型交集
                get_movie_tag_li2 = self.get_movie_tag_li(tag_name[2])
                movie_id_rs = self.add_more_tag(movie_id_rs, get_movie_tag_li2)
            if len(movie_id_rs) > 300:  # 如果第一种、第二种与第三种类型存在的结果较多则再与第四种类型交集
                get_movie_tag_li3 = self.get_movie_tag_li(tag_name[3])
                movie_id_rs = self.add_more_tag(movie_id_rs, get_movie_tag_li3)
            if len(movie_id_rs) < 5:  # 如果第一种类型与第四种类型不存在同时存在的电影就直接取第一种类型的结果
                movie_id_rs = get_movie_tag_li0
        movie_id_rs = random.sample(movie_id_rs, 5)
        return movie_id_rs

    # 根据电影推荐电影（电影详情页中）
    def get_movie_5_cai(self, movie_id):

        movie_tag_cai_rs_json = get_readis("movie_tag_cai" + "_" + str(movie_id) + "_" + str(5))
        if movie_tag_cai_rs_json:
            return movie_tag_cai_rs_json

        movie_tag_name_li = list(MovieTagDB.objects.filter(Q(tag_type='genre') & Q(movie_id_id=movie_id))
                                 .values_list("tag_name", flat=True))
        movie_id_li = self.get_5_tag_movie_id(movie_tag_name_li)
        movie_cai_rs = CollectMovieDB.objects.filter(movie_id__in=movie_id_li).all()
        movie_cai_rs_json = queryset_to_json(movie_cai_rs)

        # 设置10分钟缓存不变
        set_readis("movie_tag_cai" + "_" + str(movie_id) + "_" + str(5), movie_cai_rs_json, set_time=60 * 10)

        return movie_cai_rs_json

    # 获取系统推荐的5部电影（历史记录中，猜你喜欢） 应使用Spark中spark.py最后获取的结果
    def get_user_movie_5_cai(self, user_id):

        user_movie_tag_cai_rs_json = get_readis("user_tag_cai" + "_" + str(user_id) + "_" + str(5))
        if user_movie_tag_cai_rs_json:
            return user_movie_tag_cai_rs_json

        user_movie_recommend = UserMovieRecommend.objects.filter(user_id=user_id)
        if not user_movie_recommend.exists():
            return []
        movie_id_li = user_movie_recommend.get(user_id=user_id).movie_id_li.split("，")
        if len(movie_id_li) < 5:
            user_tag_li = UserTag.objects.filter(Q(tag_type="info_movie_type") & Q(user_id=user_id))\
                .order_by("-tag_weight").values_list("tag_name", flat=True)
            if not user_tag_li:
                user_tag_li = ["动作", "科幻", "爱情", "喜剧"]
            else:
                user_tag_li = list(user_tag_li)[:4]
            # user_api.User().getUserPreferTag(user_id).split(",")
            movie_id_li = self.get_5_tag_movie_id(user_tag_li)
        else:
            movie_id_li = random.sample(movie_id_li, 5)

        user_movie_tag_cai_rs = CollectMovieDB.objects.filter(movie_id__in=movie_id_li).all()
        user_movie_tag_cai_rs_json = queryset_to_json(user_movie_tag_cai_rs)

        # 设置10分钟缓存不变
        set_readis("user_tag_cai" + "_" + str(user_id) + "_" + str(5), user_movie_tag_cai_rs_json, set_time=60 * 10)

        return user_movie_tag_cai_rs_json
