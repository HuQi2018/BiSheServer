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
from api import captcha, email_vail, districts

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('captcha', captcha.get_code),    # 验证码
    path('districts', districts.findByParent.as_view()),    # 获取地址信息关联
    path('email_vail', email_vail.send_reg_email.as_view()),    # 发送邮箱验证码
]
