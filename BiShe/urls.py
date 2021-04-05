"""api URL Configuration

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
from django.contrib import admin
from django.urls import path, include

from BiShe import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),    # 首页
    path('index.html', views.index),    # 首页
    path('register.html', views.register),    # 注册
    path('category.html', views.category),    # 分类
    path('search.html', views.search),    # 搜索
    path('movie.html', views.movie),    # 电影详情
    path('userInfo.html', views.userInfo),    # 用户首页

]
