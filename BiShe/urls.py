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
from django.urls import path
from django.contrib import admin
from BiShe import views
# from BiShe.views import check_admin_login

urlpatterns = [
    # path('admin/', check_admin_login(admin.site.urls)),
    path('admin/', admin.site.urls),
    path('', views.index),    # 首页
    path('index.html', views.index),    # 首页
    path('register.html', views.register),    # 注册
    path('category.html', views.category),    # 分类
    path('search.html', views.search),    # 搜索
    path('movie.html', views.movie),    # 电影详情
    path('userInfo.html', views.user_info),    # 用户中心
    path('forgetPwd.html', views.foget_password),    # 忘记密码
    path('modifyPwd.html', views.modify_password),    # 修改密码
    path('modifyEmail.html', views.modify_email),    # 修改邮箱
    path('userCollection.html', views.user_collection),    # 收藏管理
    path('userComment.html', views.user_comment),    # 评论管理

]
