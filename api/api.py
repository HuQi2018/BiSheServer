# 1，首先引入hashlib模块
import hashlib
import json
import time

from api.model_json import queryset_to_json
from api.models import IndexFocus
from api.redis_pool import cache


# api方法调用
class Api:

    def __init__(self):
        pass

    @staticmethod
    def password_encrypt(pwd):
        md5 = hashlib.md5()  # 2，实例化md5() 方法
        md5.update(pwd.encode())  # 3，对字符串的字节类型加密
        result = md5.hexdigest()  # 4，加密
        return result

    @staticmethod
    def randCodeVail(request, randCode):
        rs = [True,"验证成功！"]
        try:
            request.session['reg_verify_code']
        except:
            return [False, "验证码已失效，请重新获取！"]
            # return JsonError("请先获取验证码！")
        if not randCode:
            rs = [False, "请先填写验证码！"]
        elif int(time.time() - request.session['reg_verify_code'][1]) > 3 * 60:
            del request.session['reg_verify_code']
            rs = [False, "验证码已过期，请重新获取！"]
            # return JsonError("验证码已过期！")
        elif randCode.upper() != request.session['reg_verify_code'][0].upper() or not \
                request.session['reg_verify_code'] or not randCode:
            rs = [False, "验证码不正确！"]
            # return JsonError("验证码不正确！")
        else:
            del request.session['reg_verify_code']
        return rs

    @staticmethod
    def emailCodeVail(request, emailCode, name):
        rs = [True, "验证成功！"]
        try:
            request.session[name]
        except:
            return [False, "邮件验证码已过期，请重新获取！"]
            # return JsonError("请先获取邮件验证码！")
        if not emailCode:
            rs = [False, "请先填写验证码！"]
        elif int(time.time()-request.session[name][1]) > 3*60:
            rs = [False, "邮件验证码已过期，请重新获取！"]
            # return JsonError("验证码已过期，请重新获取！")
        elif emailCode != request.session[name][0] or not request.session[name] or not emailCode:
            rs = [False, "验证码不正确！"]
            # return JsonError("验证码不正确！")
        else:
            del request.session[name]
        return rs

    @staticmethod
    def get_ip(request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ipaddress = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ipaddress = request.META['REMOTE_ADDR']
        return ipaddress

    @staticmethod
    def set_readis(key, data, set_time=60 * 60 * 24):
        try:
            cache.set(key, json.dumps(data))
            cache.expire(key, set_time)
            return 1
        except Exception as ex:
            print("存储Redis缓存失败！key："+key)
            print(ex.__str__())
            return 0

    @staticmethod
    def get_readis(key):
        try:
            data = cache.get(key)
        except Exception as ex:
            data = ""
            print("读取Redis缓存失败！key："+key)
            print(ex.__str__())
        if not data:
            return 0
        else:
            return json.loads(data.decode('utf-8'))

    @staticmethod
    def index_focus():
        index_focus_rs = IndexFocus.objects.filter(status=1).order_by("show_id").all()
        index_focus_rs_json = queryset_to_json(index_focus_rs)
        return index_focus_rs_json
