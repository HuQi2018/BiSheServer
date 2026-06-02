"""movie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from movie import views

urlpatterns = [
    path('search', views.movie_search),    # 搜索
    path('movie_rating', views.MovieRating.as_view()),    # 评分
    path('movie_like', views.MovieLike.as_view()),    # 收藏
    path('movie_comment', views.MovieComment.as_view()),    # 添加评论
    path('delete_movie_comment', views.MovieCommentDelete.as_view()),    # 删除评论
    # path('test', views.TryView.as_view()),    # get、post
]
