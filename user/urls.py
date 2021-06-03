"""user URL Configuration

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
from django.conf.urls import url
from django.urls import path

from user import views
# from .views import user_login, user_logout, user_register1, user_register2, user_register3, user_forget_password, \
#     user_info_modify, user_password_modify, user_email_modify

urlpatterns = [
    path('login', views.user_login.as_view()),    # 登录
    path('logout', views.user_logout.as_view()),    # 注销
    path('register1', views.user_register1.as_view()),    # 注册第一步
    path('register2', views.user_register2.as_view()),    # 注册第二步
    path('register3', views.user_register3.as_view()),    # 注册第三步
    path('fget', views.user_forget_password.as_view()),    # 忘记密码
    path('infoModify', views.user_info_modify.as_view()),    # 修改用户信息
    path('pwdModify', views.user_password_modify.as_view()),    # 修改密码
    path('emailModify', views.user_email_modify.as_view()),    # 修改邮箱
    url(r'^user_img/(?P<user_id>.+)/$',views.user_img,name="image"),   # 用户头像api
    # path('test', views.TryView.as_view()),    # get、post
]
