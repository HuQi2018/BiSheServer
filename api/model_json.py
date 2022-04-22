
# 将查询出的结果集转换为json
# 遍历查询集 调用model属性转换成dict
import datetime
# import json
# from django.core import serializers
from django.db.models import Model


def model_to_json(self):
    # 简化，但不支持时间转
    # return dict([(attr, getattr(self, attr)) for attr in
    #              [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
    # 增强加入时间转
    # need_json = ['rating', 'pubdates', 'countries', 'aka', 'tags', 'durations', 'genres', 'videos', 'images',
    #              'photos', 'languages', 'writers', 'actor', 'summary', 'directors']
    # fields = []
    # for field in self._meta.fields:
    #     fields.append(field.name)
    d = {}
    for attr in self._meta.fields:
        obj = getattr(self, attr.name)
        if isinstance(obj, datetime.datetime):
            rs = obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            rs = obj.strftime("%Y-%m-%d")
        elif obj.__class__.__name__ == 'UsersBase':
            rs = obj.id
        elif obj.__class__.__name__ == 'CollectMovieDB':
            if self.__class__.__name__ == 'MovieComments':
                rs = obj.movie_id
            else:
                rs = obj.title
        elif isinstance(obj, Model):
            rs = obj.__str__()
        elif obj is None:
            rs = ""
        elif obj is True:
            rs = "true"
        elif obj is False:
            rs = "true"
        else:
            rs = obj
        # if attr in need_json:
        #     print(rs)
        #     print(type(rs))
        #     # rs = serializers.serialize('json', rs)
        #     rs = json.loads(rs.replace("'",'"'))
        #     print(rs)
        #     print(type(rs))
        d[attr.name] = rs
    return d


def queryset_to_json(queryset):
    obj_arr = []
    for o in queryset:
        obj_arr.append(o.toDict())
    return obj_arr

# def convert_obj_to_json(queryset):
#     str_json = serializers.serialize('json', queryset)
#     print(str_json)
#     return json.dumps(str_json, ensure_ascii=False)

# 获取model中的所有数据
# def get_model_json(model,modules_field_name_list):
#     serialize_model_values = []
#     params = model._meta.fields
#     for t in range(len(params)):
#         modules_field_name_list.append(params[t].name)#获取字段名称
#     model_values = model.objects.all().values(*modules_field_name_list)#获取modules_field_name_list列表字段数据
#     for value in model_values:
#         serialize_model_values.append(value)
#     json_data = json.dumps(serialize_model_values)
#     return json_data
#
#
# def get_model_field_name_all(model):
#     modules_field_name_list = []
#     params = model._meta.fields
#     for t in range(len(params)):
#         modules_field_name_list.append(params[t].name)#获取字段名称
#     return modules_field_name_list
#
#
# def get_model_verbose_name_all(model):
#     modules_verbose_name_list = []
#     params = model._meta.fields
#     for t in range(len(params)):
#         modules_verbose_name_list.append(params[t].verbose_name)#获取字段自定义名称
#     return modules_verbose_name_list
