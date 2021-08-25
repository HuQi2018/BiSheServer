import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q

from BiSheServer import settings
from api.model_json import queryset_to_json
from user.models import UsersPerfer, UsersDetail, UserTag


# 用户api
class User:

    def __init__(self):
        pass

    # 获取用户喜欢的电影类型
    @staticmethod
    def getUserPreferTag(user_id):
        user_prefer_tag_rs = UsersDetail.objects.filter(user_id_id=user_id).values_list("user_prefer", flat=True)[0]
        if not user_prefer_tag_rs:
            return ""
        return user_prefer_tag_rs

    # 获取用户的兴趣爱好
    @staticmethod
    def getUserHobbiesTag(user_id):
        user_obbies_tag_rs = UsersDetail.objects.filter(user_id_id=user_id).first().values("user_hobbies")
        if not user_obbies_tag_rs:
            return ""
        return user_obbies_tag_rs

    # 获取所有的爱好标签
    @staticmethod
    def getHobbiesTag():
        hobbies_tag_rs = UsersPerfer.objects.all()
        return hobbies_tag_rs

    def getHobbiesTagJson(self):
        hobbies_tag_rs = queryset_to_json(self.getHobbiesTag().all())
        return hobbies_tag_rs

    # 添加用户的标签
    @staticmethod
    def add_user_tag(user_id, tag_type, tag_name, tag_weight):
        # 除评论和评分标签外，所有标签初始化创建时初始设置为5
        if tag_type != "rating_movie_id" and tag_type != "comment_movie_id" and tag_type != "info_movie_tag":
            UserTag.objects.create(user_id=user_id, tag_type=tag_type, tag_name=tag_name, tag_weight=5)
        else:
            if tag_type == "info_movie_tag":  # 电影标签默认一律为2
                tag_weight = 2
            UserTag.objects.create(user_id=user_id, tag_type=tag_type, tag_name=tag_name, tag_weight=tag_weight)

    # 修改用户的标签权重
    def modify_user_tag(self, user_id, tag_type, tag_name, tag_weight):
        user_tag = UserTag.objects.filter(Q(user_id=user_id) & Q(tag_type=tag_type) & Q(tag_name=tag_name))
        if user_tag.exists():  # 存在该标签则进行修改
            if type(tag_weight) == str:  # 判断其为修改标签权值，如果为数字则直接对其进行赋值
                old_tag_weight = int(user_tag.first().tag_weight)
                try:
                    tag_weight = int(tag_weight)
                except Exception as ex:
                    print("非法权值！" + ex.__str__())
                    return ""
                if old_tag_weight != 0:  # 修改标签权值
                    tag_weight = old_tag_weight + tag_weight
                else:  # 第二次添加标签
                    tag_weight = 5 + tag_weight
            user_tag.update(tag_weight=str(tag_weight))
        else:
            self.add_user_tag(user_id, tag_type, tag_name, tag_weight)

    # 检查用户是否登录
    @staticmethod
    def isNotLogin(request):
        try:
            if not request.session['is_login'] or not request.session['user_id']:
                raise Exception
        except:
            return True

    # 用户头像上传
    @staticmethod
    def userImageUpload(user_img):
        rs = []
        imgName = uuid.uuid4().hex
        img_size = user_img.size
        img_name = user_img.name
        img_ext = '.' in img_name and img_name.rsplit('.', 1)[-1]

        # print(img_size)
        # 判断文件后缀是否在列表中
        def allowed_file(img_ext):
            return img_ext in settings.default['allow_extensions']

        if user_img:
            if not allowed_file(img_ext):
                rs = [False,"非图片类型上传！"]
                # return JsonError("非图片类型上传！")
            elif img_size > int(settings.default['allow_maxsize']):
                rs = [False, "图片大小超过5MB，上传失败！"]
                # return JsonError("图片大小超过5MB，上传失败！")
            else:
                img_path = default_storage.save(settings.default['avatars_upload_folder'] + imgName + "." + img_ext,
                                            ContentFile(user_img.read()))  # 保存文件
                # request.session['user_img'] = img_path
                rs = [True, img_path]
        return rs

