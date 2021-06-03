import datetime
import os

from django.http import HttpResponse

from BiSheServer import settings
from user.models import UsersBase, UsersDetail, UserCookie
from django.db.models import Q
from api import api, user_api, delay_work
import re
import uuid
from rest_framework.views import APIView
from api.response import JsonError, JsonResponse

match_phone = re.compile(r'^1(3\d|5[0-35-9]|8[025-9]|47)\d{8}$')
match_name = re.compile(r'^[\u4E00-\u9FA5a-zA-Z][\u4E00-\u9FA5a-zA-Z0-9_]*$')
match_mail = re.compile(r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$')
# match_passwd = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$')
match_passwd = re.compile(r'^[\x21-\x7e]{6,20}$')
match_randCode = re.compile(r'^[A-Za-z\d]{4}$')
match_age = re.compile(r'^[\d]{1,3}$')
match_birthday = re.compile(r'^[\d]{4}-[\d]{2}-[\d]{2}$')
match_prefer = re.compile(r'^([\u4E00-\u9FA5]*,)*[\u4E00-\u9FA5]*$')
match_gender = re.compile(r'^[0-2]$')

Api = api.Api()
User = user_api.User()

isNotLogin = User.isNotLogin
userImageUpload = User.userImageUpload

md5 = Api.password_encrypt
randCodeVail = Api.randCodeVail
emailCodeVail = Api.emailCodeVail
get_ip = Api.get_ip
tag_thread_work = delay_work.tag_thread_work


# Create your views here.
# 用户登录
class user_login(APIView):
    def get(self, request, *args, **kwargs):
        return JsonError("不支持Get请求！")

    def post(self, request, *args, **kwargs):
        request.session.flush()  # 先清除原有记录
        user_count = request.POST.get("username")
        user_password = request.POST.get("password")
        user_rs = UsersBase.objects.filter(Q(user_name=user_count) | Q(user_mail=user_count))  # .values("user_passwd")
        if user_rs.exists():
            user_rs = user_rs.first()
            if md5(user_password) == user_rs.user_passwd:
                # print(user_rs.user_name)
                request.session['user_name'] = user_rs.user_name
                request.session['user_uname'] = user_rs.user_uname
                request.session['user_id'] = user_rs.id
                request.session['user_role'] = user_rs.user_role
                request.session['user_email'] = user_rs.user_mail
                request.session['user_status'] = user_rs.user_status
                request.session['user_reg_step'] = user_rs.user_reg_step
                if int(user_rs.user_reg_step) == 1:
                    return JsonResponse({"msg": "您还未完成账号验证，即将跳转至账号验证！", "url": "register.html"})
                if int(user_rs.user_status) != 1:
                    request.session.flush()
                    return JsonError("您的账号状态不正常，不可使用请咨询管理员！")
                # 判断是否为新账号登录，新账号登录则更换uuid
                # user_uuid = request.COOKIES.get("uuid") if request.COOKIES.get("uuid") else uuid.uuid4().hex
                # cookie_uuid = request.COOKIES.get("uuid")
                # if not cookie_uuid:
                #     cookie_uuid = uuid.uuid4().hex
                #     # request.COOKIES["uuid"] = cookie_uuid
                cookie_uuid = uuid.uuid4().hex
                request.session['user_uuid'] = cookie_uuid
                request.session['user_img'] = user_rs.user_img
                # print(user_rs.user_img)
                request.session['is_login'] = True
                user_agent = request.environ.get("HTTP_USER_AGENT")
                user_ip = get_ip(request)
                UserCookie.objects.create(user_id=user_rs.id, user_agent=user_agent, cookie_uuid=cookie_uuid,
                                          user_ip=user_ip)
                return JsonResponse({"msg": "登陆成功！", "url": "?", "uuid": cookie_uuid})
            else:
                return JsonError("登录账号或密码不正确！")
        else:
            return JsonError("登录账号或密码不正确！")


# 用户注销
class user_logout(APIView):
    def get(self, request, *args, **kwargs):
        try:
            if request.session['is_login']:  # 如果已登录则注销
                uuid = request.session.get("user_uuid")
                request.session.flush()
                UserCookie.objects.filter(cookie_uuid=uuid)\
                    .update(quit_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                # return HttpResponseRedirect('')  #跳转到index界面
                return JsonResponse({"msg": "注销成功！", "url": "/", "uuid": uuid})
                # return JsonResponse({"msg": "注销成功！", "url": "/" })
            else:
                return JsonError("您还未登陆！")
        except Exception as e:
            return JsonError("您还未登陆！")

    def post(self, request, *args, **kwargs):
        return JsonError("不支持POST请求！")


# 用户注册第一步
class user_register1(APIView):
    def get(self, request, *args, **kwargs):
        return JsonError("不支持Get请求！")

    def post(self, request, *args, **kwargs):
        try:
            if request.session['is_login'] :
                request.sessions.flush()
        except Exception as e:
            pass
            # request.session.set_expiry(10)
            # del request.session['pass']

        user_name = request.POST.get("user_name")
        user_mail = request.POST.get("user_mail")
        user_phone = request.POST.get("user_phone")
        user_gender = request.POST.get("sex") if request.POST.get("sex") else 0
        user_passwd = request.POST.get("user_passwd")
        randCode = request.POST.get("randCode")

        if match_phone.match(user_phone) and match_name.match(user_name) and \
                (not user_gender or match_gender.match(user_gender)) and match_mail.match(user_mail) \
                and match_passwd.match(user_passwd) and match_randCode.match(randCode):
            if UsersBase.objects.filter(user_name=user_name).exists():
                return JsonError("用户名已存在，请更换！")
            elif UsersBase.objects.filter(Q(user_mail=user_mail) & Q(user_status=1)).exists():
                return JsonError("邮箱已存在，请更换！")
            elif UsersBase.objects.filter(user_phone=user_phone).exists():
                return JsonError("电话已存在，请更换！")
            # elif str(randCode).upper() != str(cache.get("reg_verify_code").decode('utf-8')).upper() :
            #     print(randCode,str(cache.get("reg_verify_code").decode('utf-8')))

            randCodeVailRs = randCodeVail(request, randCode)
            if not randCodeVailRs[0]:
                return JsonError(randCodeVailRs[1])

            user = UsersBase.objects.create(user_name=user_name, user_uname=user_name, user_mail=user_mail,
                                            user_phone=user_phone, user_gender=user_gender,
                                            user_passwd=md5(user_passwd), user_reg_step=1)
            UsersDetail.objects.create(user_id=user)

            tag_thread_work("user_info_tag", user_id=user.id, user_phone=user_phone, user_gender=user_gender)

            request.session['user_name'] = user_name
            request.session['user_id'] = user.id
            request.session['user_email'] = user_mail
            request.session['user_status'] = 0
            request.session['user_reg_step'] = 1
            # del request.session['reg_verify_code']
            request.session['reg_verify_code'] = ""

            # request.session['user_img'] = "static/images/user.jpg"
            # user.save()
            # print(user)UsersBase object (2)
            # print(user.id) 2
            # for key, value in request.POST.items():
            #     print('Key: %s Value %s' % (key,value))
            return JsonResponse({"msg": "第一步注册成功！", "email": user_mail, "userName": user_name})
        else:
            return JsonError("注册失败，请检查输入的信息是否正确！")


# 用户注册第二步
class user_register2(APIView):
    def get(self, request, *args, **kwargs):
        return JsonError("不支持Get请求！")

    def post(self, request, *args, **kwargs):
        emailCode = request.POST.get("emailCode")
        # user_id = request.session.get('user_reg_step')
        # user = UsersBase.objects.get(id=user_id)
        try:
            request.session.get('user_reg_step')
        except:
            return JsonError("请先完成第一步注册操作！")

        if request.session.get('user_reg_step') == 2:
            return JsonError("你已完成第二步注册，请直接登录！")
        emailCodeVailRs = emailCodeVail(request, emailCode, "email_verify_code")
        if not emailCodeVailRs[0]:
            return JsonError(emailCodeVailRs[1])
        else:
            user_mail = request.session['user_email']
            user = UsersBase.objects.filter(id=request.session.get('user_id')).update(user_reg_step=2, user_status=1,
                                                                                      user_mail=user_mail)  # 此时账号可用
            request.session['user_status'] = 1
            # request.session['is_login'] = True
            request.session['user_reg_step'] = 2
            # request.session['email_verify_code'] = ""
            return JsonResponse({"msg": "第二步验证成功！"})


# 用户注册第三步
class user_register3(APIView):
    def get(self, request, *args, **kwargs):
        return JsonError("不支持Get请求！")

    def post(self, request, *args, **kwargs):
        user_age = request.POST.get("user_age") if request.POST.get("user_age") else 0
        user_uname = request.POST.get("user_uname")
        user_birthday = request.POST.get("user_birthday") if request.POST.get("user_birthday") else None
        user_address = request.POST.get("user_address")
        user_province = request.POST.get("provinceName")
        user_city = request.POST.get("cityName")
        user_district = request.POST.get("districtName")
        user_prefer = request.POST.get("user_prefer")
        user_hobbies = request.POST.get("user_hobbies")
        user_img = request.FILES.get("user_img")

        # for key, value in request.POST.items():
        #     print('Key: %s Value %s' % (key,value))
        if (not user_age or match_age.match(user_age)) and (not user_birthday or match_birthday.match(user_birthday))\
                and (not user_address or match_name.match(user_address)) and (not user_province or match_name.match(user_province))\
                and (not user_city or match_name.match(user_city)) and (not user_district or match_name.match(user_district))\
                and (not user_prefer or match_prefer.match(user_prefer)) and (not user_hobbies or match_prefer.match(user_hobbies))\
                and (not user_uname or match_name.match(user_uname)):

            try:
                user_id = request.session['user_id']
            except:
                return JsonError("请先完成第一步注册操作！")

            user = UsersBase.objects.get(id=user_id)
            if user.user_reg_step == 3:
                return JsonError("你已完成第三步注册，请直接登录！")
            if user_img:
                user_img_rs = userImageUpload(user_img)
                if user_img_rs[0]:
                    img_path = user_img_rs[1]
                else:
                    return JsonError(user_img_rs[1])
            else:
                img_path = "static/images/user.jpg"
            if not user_uname:
                user_uname = request.session['user_name']

            UsersBase.objects.filter(id=user_id).update(user_reg_step=3, user_img=img_path, user_uname=user_uname)
            if not UsersDetail.objects.filter(user_id=user).exists():
                UsersDetail.objects.create(user_id=user)
                # return JsonError("注册失败，请重新注册！")
            UsersDetail.objects.filter(user_id=user).update(user_age=user_age, user_birthday=user_birthday,
                                                            user_address=user_address, user_province=user_province,
                                                            user_city=user_city,  user_district=user_district,
                                                            user_prefer=user_prefer, user_hobbies=user_hobbies)

            tag_thread_work("user_info_tag", user_id=user_id, user_age=user_age, user_province=user_province,
                            user_city=user_city, user_prefer=user_prefer, user_hobbies=user_hobbies)

            # request.session['user_uname'] = user_uname
            # request.session['user_img'] = img_path
            request.session.flush()  # 清除所有信息准备登陆
            return JsonResponse({"msg": "第三步完成信息成功！"})
        else:
            return JsonError("提交失败，请检查输入的信息是否正确！")


# 用户忘记密码
class user_forget_password(APIView):
    def get(self, request, *args, **kwargs):
        return JsonError("不支持Get请求！")

    def post(self, request, *args, **kwargs):
        try:
            fget_step = int(request.GET.get("step"))
        except:
            return JsonError("请求参数不正确！")
        if fget_step == 1:  # 账户验证
            user_name = request.POST.get("user_name")
            # user_mail = request.POST.get("user_mail")
            randCode = request.POST.get("randCode")

            randCodeVailRs = randCodeVail(request, randCode)
            if not randCodeVailRs[0]:
                return JsonError(randCodeVailRs[1])

            if match_name.match(user_name):
                user_rs = UsersBase.objects.filter(user_name=user_name)  # .values("user_passwd")
                if user_rs.exists():
                    user_rs = user_rs.first()
                    user_email = user_rs.user_mail
                    user_mail = user_email[:3]+"***"+user_email[(int(len(user_email)/2)):]
                    request.session['fget_step_code'] = 1
                    request.session['user_mail'] = user_mail    # 加密后的邮箱
                    request.session['user_fget_email'] = user_email  # 未加密的邮箱
                    # request.session['reg_verify_code'] = ""
                    return JsonResponse({"msg": "账户验证成功！", "email": user_mail})
                else:
                    return JsonError("用户名不存在！")
            else:
                return JsonError("请检查用户名是否正确！")

        elif fget_step == 2:  # 邮箱验证
            try:
                request.session['fget_step_code']
            except:
                return JsonError("请先完成第一步账户验证！")

            if request.session['fget_step_code'] == 1:
                user_mail = request.POST.get("user_mail")
                emailCode = request.POST.get("emailCode")

                emailCodeVailRs = emailCodeVail(request, emailCode, "email_fget_verify_code")
                if not emailCodeVailRs[0]:
                    return JsonError(emailCodeVailRs[1])
                if match_mail.match(user_mail):
                    if request.session['user_fget_email'] == user_mail:
                        request.session['fget_step_code'] = 2
                        # request.session['email_fget_verify_code'] = ""
                        return JsonResponse({"msg": "邮箱验证成功！"})
                    else:
                        return JsonError("邮箱不正确！")
                else :
                    return JsonError("请检查邮箱是否正确！")
            else:
                return JsonError("请先完成第一步账户验证！")

        elif fget_step == 3:  # 密码修改
            try:
                request.session['fget_step_code']
            except:
                return JsonError("请先完成前两步验证！")
            if request.session['fget_step_code'] == 2:
                user_passwd = md5(request.POST.get("user_passwd"))
                user_mail = request.session['user_fget_email']

                UsersBase.objects.filter(user_mail=user_mail).update(user_passwd=user_passwd)
                request.session.flush()
                return JsonResponse({"msg": "密码修改成功！"})
            else:
                return JsonError("请先完成前两步验证！")
        else:
            return JsonError("修改失败，请检查输入的信息是否正确！")


# 用户修改个人信息
class user_info_modify(APIView):
    def get(self, request, *args, **kwargs):
        return JsonError("不支持Get请求！")

    def post(self, request, *args, **kwargs):
        if isNotLogin(request):
            return JsonError("请先登录！")
        user_img = request.FILES.get("user_img")
        user_phone = request.POST.get("user_phone")
        user_gender = request.POST.get("sex")
        user_uname = request.POST.get("user_uname")
        user_age = request.POST.get("user_age") if request.POST.get("user_age") else 0
        user_birthday = request.POST.get("user_birthday") if request.POST.get("user_birthday") else None
        user_province = request.POST.get("provinceName")
        user_city = request.POST.get("cityName")
        user_district = request.POST.get("districtName")
        user_address = request.POST.get("user_address")
        randCode = request.POST.get("randCode")
        user_prefer = request.POST.get("user_prefer")
        user_hobbies = request.POST.get("user_hobbies")


        if (not user_age or match_age.match(user_age)) and (not user_birthday or match_birthday.match(user_birthday))\
                and (not user_address or match_name.match(user_address)) and (not user_province or match_name.match(user_province))\
                and (not user_city or match_name.match(user_city)) and (not user_district or match_name.match(user_district))\
                and (not user_prefer or match_prefer.match(user_prefer)) and (not user_hobbies or match_prefer.match(user_hobbies))\
                and (not user_uname or match_name.match(user_uname)) and (not user_gender or match_gender.match(user_gender)) \
                and (not user_phone or match_phone.match(user_phone)) and (not randCode or match_randCode.match(randCode)):

            randCodeVailRs = randCodeVail(request, randCode)
            if not randCodeVailRs[0]:
                return JsonError(randCodeVailRs[1])

            user_id = request.session['user_id']

            if user_img:
                user_img_rs = userImageUpload(user_img)
                if user_img_rs[0]:
                    img_path = user_img_rs[1]
                    request.session['user_img'] = img_path
                else:
                    return JsonError(user_img_rs[1])
            else:
                img_path = request.session['user_img']
            request.session['user_uname'] = user_uname

            user = UsersBase.objects.filter(id=user_id).update(user_img=img_path, user_uname=user_uname,
                                                               user_phone=user_phone, user_gender=user_gender)
            user2 = UsersDetail.objects.filter(user_id_id=user_id).update(user_age=user_age,
                                                                          user_birthday=user_birthday,
                                                                          user_address=user_address,
                                                                          user_district=user_district,
                                                                          user_province=user_province,
                                                                          user_city=user_city,
                                                                          user_prefer=user_prefer,
                                                                          user_hobbies=user_hobbies)

            # 用户每修改一次，则代表信息越准确，将其权值+1
            tag_thread_work("user_info_tag", user_id=user_id, user_age=user_age, user_province=user_province,
                            user_city=user_city, user_prefer=user_prefer, user_hobbies=user_hobbies,
                            user_phone=user_phone, user_gender=user_gender, tag_weight="+1")

            return JsonResponse({"msg": "用户信息修改成功！", "url": "?"})
        else:
            return JsonError("修改失败，请检查输入的信息是否正确！")


# 用户修改密码
class user_password_modify(APIView):
    def get(self, request, *args, **kwargs):
        return JsonError("不支持Get请求！")

    def post(self, request, *args, **kwargs):
        if isNotLogin(request):
            return JsonError("请先登录！")
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        user_id = request.session['user_id']
        randCode = request.POST.get("randCode")

        if old_password and match_passwd.match(new_password) and match_randCode.match(randCode):

            randCodeVailRs = randCodeVail(request, randCode)
            if not randCodeVailRs[0]:
                return JsonError(randCodeVailRs[1])

            old_password = md5(old_password)
            new_password = md5(new_password)
            user = UsersBase.objects.get(id=user_id)
            if user.user_passwd != old_password:
                return JsonError("原密码错误！")
            else:
                UsersBase.objects.filter(id=user_id).update(user_passwd=new_password)
                return JsonResponse({"msg": "密码修改成功！", "url": "?", })
        else:
            return JsonError("修改失败，请检查输入的信息是否正确！")


# 用户修改邮箱
class user_email_modify(APIView):
    def get(self, request, *args, **kwargs):
        return JsonError("不支持Get请求！")

    def post(self, request, *args, **kwargs):
        if isNotLogin(request):
            return JsonError("请先登录！")
        user_mail = request.POST.get("user_mail")
        user_id = request.session['user_id']
        emailCode = request.POST.get("emailCode")
        if match_mail.match(user_mail):

            emailCodeVailRs = emailCodeVail(request, emailCode, "email_modify_verify_code")
            if not emailCodeVailRs[0]:
                return JsonError(emailCodeVailRs[1])
            else:
                UsersBase.objects.filter(id=user_id).update(user_mail=user_mail)
                request.session['user_email'] = user_mail
                return JsonResponse({"msg": "邮箱修改成功！", "url": "?", })
        else:
            return JsonError("修改失败，请检查输入的信息是否正确！")


# 用户头像读取
def user_img(request, user_id):
    """
    : 读取图片
    :param request:
    :return:
    """
    try:
        # user_id = request.GET.get("id")
        user = UsersBase.objects.values("user_img").get(id=user_id)
        imagepath = os.path.join(settings.BASE_DIR, "{}".format(user["user_img"]))  # 图片路径
        with open(imagepath, 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/png")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))
