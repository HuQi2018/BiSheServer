from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)



# # 插入数据
# Obj=UserInfo(name="jay",password="abc123")
# Obj.name="john"
# Obj.save()
#
# # 查询数据
# UserInfo.objects.all()  # 查询表中的所有记录
# UserInfo.objects.filter(name_contains='j')  # 查询表中name含有“j”的所有记录,被使用较多
# UserInfo.objects.get(name="john")  # 有且只有一个查询结果，如果超出一个或者没有,则抛出异常
# UserInfo.objects.get(name="john").delete()  # 删除名字为john的记录
# UserInfo.objects.get(name="john").update(name='TOM')  # 更新数据表的name为TOM