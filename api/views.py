from django.shortcuts import render
import requests
from django.http import HttpResponse, HttpResponseBadRequest

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


def proxy_image(request):
    """图片代理视图，用于处理豆瓣图片的请求"""
    url = request.GET.get('url')
    if not url:
        return HttpResponseBadRequest('Missing URL parameter')
    
    # 检查是否是豆瓣图片URL
    if 'doubanio.com' not in url and 'douban.com' not in url:
        return HttpResponseBadRequest('Only Douban images are allowed')
    
    try:
        # 设置合适的请求头，模拟浏览器请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/62.0.3202.94 Safari/537.36',
            'Referer': 'https://movie.douban.com/'
        }
        # 发送请求获取图片
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        # 检查响应状态码
        if response.status_code != 200:
            return HttpResponse(f'Error fetching image: {response.status_code}', status=response.status_code)
        
        # 获取图片内容和Content-Type
        content = response.content
        content_type = response.headers.get('Content-Type', 'image/jpeg')
        
        # 返回图片响应
        return HttpResponse(content, content_type=content_type)
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)
