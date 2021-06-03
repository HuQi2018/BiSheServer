"""test URL Configuration

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

from TestServer.views import user_register1,TryView,logout,movie_collections, try_get

urlpatterns = [
    path('login', user_register1.as_view()),    # 验证码
    path('logout', logout.as_view()),    # 验证码
    path('test', TryView.as_view()),    # get、post
    path('movie', movie_collections),    # get、post
    path('tryGet', try_get),    # get、post
]
