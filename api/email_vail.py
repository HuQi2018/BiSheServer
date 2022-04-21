from BiSheServer.settings import CONFIG
from api import user_api, api
from api.redis_pool import cache
from rest_framework.views import APIView
from api.response import JsonError, JsonResponse
from user.models import UsersBase
from .email import send_reg_email as send_email
from django.db.models import Q
import string, random, time, re


class send_reg_email(APIView):
    def get(self, request, *args, **kwargs):
        return JsonError("不支持Get请求！")

    def post(self, request, *args, **kwargs):
        user_email = request.POST.get("email")

        match_mail = re.compile(r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$')
        if not match_mail.match(user_email) or not user_email:
            return JsonError("邮箱格式不正确，请检查！")

        try:
            send_type = int(request.GET.get("type"))
        except:
            return JsonError("请求参数不正确！")

        # cache.set('email_verify_code',email_verify_code)
        # cache.expire('email_verify_code', 60 * 3)
        # request.session['email_verify_code'].set_expiry(60*3)
        email_verify_code = "".join(random.sample([x for x in string.digits], 6))

        if send_type == 1:  # 注册验证
            try:
                if request.session['user_reg_step'] != 1:
                    raise Exception
            except:
                return JsonError("请先完成第一步注册！")
            if UsersBase.objects.filter(Q(user_mail=user_email)).exclude(user_reg_step=1).exists():
                return JsonError("邮箱已存在，请更换！")
            title = "注册验证邮件"
            request.session['email_verify_code'] = [email_verify_code, time.time()]  # code加入到session中
            contents = '<table class="email-width" align="center" width="500" border="0" cellpadding="0" cellspacing="0" \
            role="presentation" style="width:500px;"><tbody><tr><td style="color:#505050; font-family:adobe-clean, Helvetica \
            Neue, Helvetica, Verdana, Arial, sans-serif; font-size:18px; line-height:26px; padding-top:65px;">您的验证码为：<br><br> \
            <strong style="font-size:28px; line-height:32px;">'+email_verify_code+'</strong><br><br>有效期3分钟，感谢您的注册加入。 \
            </td></tr></tbody></table>'
            request.session['user_email'] = user_email
        elif send_type == 2:  # 忘记密码验证
            try:
                if request.session['fget_step_code'] != 1:
                    raise Exception
            except:
                return JsonError("请先完成第一步操作！")
            if request.session['user_fget_email'] != user_email:
                return JsonError("邮箱不正确！")
            title = "忘记密码验证邮件"
            request.session['email_fget_verify_code'] = [email_verify_code, time.time()]  # code加入到session中
            contents = '<table class="email-width" align="center" width="500" border="0" cellpadding="0" cellspacing="0" \
            role="presentation" style="width:500px;"><tbody><tr><td style="color:#505050; font-family:adobe-clean, Helvetica \
            Neue, Helvetica, Verdana, Arial, sans-serif; font-size:18px; line-height:26px; padding-top:65px;">您的验证码为：<br><br> \
            <strong style="font-size:28px; line-height:32px;">'+email_verify_code+'</strong><br><br>有效期3分钟，感谢您的使用。 \
            </td></tr></tbody></table>'
        elif send_type == 3:  # 更改邮箱验证
            if user_api.User().isNotLogin(request):
                return JsonError("请先登录！")

            randCodeVailRs = api.Api().randCodeVail(request, request.POST.get("randCode"))
            if not randCodeVailRs[0]:
                return JsonError(randCodeVailRs[1])

            if UsersBase.objects.filter(Q(user_mail=user_email)).exists():
                return JsonError("邮箱已存在，请更换！")
            title = "更改邮箱信息验证邮件"
            request.session['email_modify_verify_code'] = [email_verify_code, time.time()]  # code加入到session中
            contents = '<table class="email-width" align="center" width="500" border="0" cellpadding="0" cellspacing="0" \
            role="presentation" style="width:500px;"><tbody><tr><td style="color:#505050; font-family:adobe-clean, Helvetica \
            Neue, Helvetica, Verdana, Arial, sans-serif; font-size:18px; line-height:26px; padding-top:65px;">您的验证码为：<br><br> \
            <strong style="font-size:28px; line-height:32px;">' + email_verify_code + '</strong><br><br>有效期3分钟，感谢您的使用。 \
            </td></tr></tbody></table>'
        else:
            return JsonError("请求参数不正确！")

        if not cache.get(user_email):
            cache.set(user_email, 1)
            cache.expire(user_email, 60 * 60 * 24)
        elif int(cache.get(user_email).decode('utf-8')) <= 2:
            cache.set(user_email, int(cache.get(user_email).decode('utf-8')) + 1, cache.ttl(user_email))
        else:
            return JsonError("该邮箱发送次数已超限制，请改日再试！")

        if CONFIG.get('EMAIL', 'EMAIL_USE') == 'False':
            return JsonResponse({"msg": "验证码发送成功！邮箱验证码为：" + str(email_verify_code)})

        try:
            send_email(user_email, title, contents)
        except Exception as e:
            # print(e)
            return JsonError("发送失败，请确认邮箱地址正确后重试！")
        return JsonResponse({"msg": "验证码发送成功！"})
