from rest_framework.views import APIView

from api.model_json import queryset_to_json
from api.response import JsonError, JsonResponse
from .models import districts


# 查询地址api
class findByParent(APIView):
    def get(self, request, *args, **kwargs):
        districts_parent = request.GET.get("parent")
        try:
            districts_parent = int(districts_parent)
        except:
            return JsonError("请检查请求参数是否正确！")
        districts_rs = districts.objects.filter(parent=districts_parent)
        if districts_rs.exists():
            rs_set = districts_rs.all()
            data = queryset_to_json(rs_set)
            return JsonResponse(data)
        else:
            return JsonError("不存在该数据！")

    def post(self, request, *args, **kwargs):
        return JsonError("不支持Post请求！")
