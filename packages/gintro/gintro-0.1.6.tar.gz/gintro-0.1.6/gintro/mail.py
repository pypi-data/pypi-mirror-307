import smtplib
from email.mime.text import MIMEText
from email.header import Header
from .decorators import timeit


@timeit
def send_mail(body, receivers):
    message = MIMEText(body, 'plain', 'utf-8')
    message['From'] = Header("SJF的AI助手", 'utf-8')  # 发件人昵称
    message['To'] = Header("投资早报订阅人", 'utf-8')  # 收件人昵称
    message['Subject'] = Header('投资早报', 'utf-8')  # 邮件主题

    # SMTP服务器信息
    smtp_server = 'smtp.126.com'
    port = 587  # 端口号，SSL连接使用465或994
    sender = 'qtnewera@126.com'
    password = 'ZKyb3pHj2gAQAbai'

    # 发送邮件
    try:
        server = smtplib.SMTP_SSL(smtp_server, port)  # 连接到SMTP服务器
        server.login(sender, password)  # 登录验证
        server.sendmail(sender, receivers, message.as_string())  # 发送邮件
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(f"邮件发送失败，错误信息：{e.smtp_error.decode('gbk')}")
    finally:
        server.quit()  # 断开服务器连接

# body = "hello world!"
# mail_list = [
#     'sweetfishhcl@sina.com'
# ]
# send_mail(body, receivers=mail_list)
