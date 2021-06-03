import yagmail
from BiSheServer import settings

# 用服务器、用户名、密码实例化邮件
mail = yagmail.SMTP(user=settings.CONFIG.get("EMAIL", "EMAIL_USER"), password=settings
                    .CONFIG.get("EMAIL", "EMAIL_PASSWORD"), host=settings.CONFIG.get("EMAIL", "EMAIL_HOST"))


def send_reg_email(reciver, title, contents):
    # 待发送的内容
    # contents = ['第一段内容', '第二段内容']
    # 发送邮件
    mail.send(reciver, title, contents)
