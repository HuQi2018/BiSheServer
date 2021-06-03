from django.shortcuts import render

from api import movie_api

data = dict()
data["movie_tag"] = movie_api.Movie().get_movie_tag()


def page_not_found(request, exception):
    return render(request, 'tempate.html', {"tip": "404错误，网页地址信息错误，请检确认无误后访问！", "url": "/", "time": 3,
                                            "title": "404错误页面", "data": data}, status=404)
    # return render(request, 'page/404.html', {"status": 404}, status=404)


def page_error(request):
    return render(request, 'tempate.html', {"tip": "500错误，服务端出错，请联系系统管理员！", "url": "/", "time": 3,
                                            "title": "500错误页面", "data": data}, status=500)
    # return render(request, 'page/500.html', {"status": 500}, status=500)
