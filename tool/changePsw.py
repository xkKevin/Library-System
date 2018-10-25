# encoding: utf-8

"""
@version: 1.0
@author: WangNing
@license: GUN
@contact:
@site:
@software: PyCharm
@file: email.py
@time: 2018/10/16 12:42
@describe: 发信模块
"""
import smtplib
from email.mime.text import MIMEText


class SendEmail:
    statue = False
    smtp = None
    msg = None

    def __init__(self):
        if self.smtp is None:
            self.login()

    def login(self, port=465, email_server='smtp.163.com', user_name="hongbaoyzm@163.com", password="asd123456789"):
        if self.smtp:
            try:
                self.smtp.close()
            except:
                pass
        try:
            self.smtp = smtplib.SMTP_SSL(email_server, port, 'localhost')
            self.smtp.helo(email_server)
            self.smtp.ehlo(email_server)
            self.smtp.login(user_name, password)
            self.statue = True
        except smtplib.SMTPException:
            print('登录失败！')
            return False
        return True

    def send(self, subject, content, receiver, sender='hongbaoyzm@163.com'):
        if not self.statue:
            print("请先登录")
            return False
        self.msg = MIMEText(content, 'plain', 'utf-8')
        self.msg['From'] = sender
        self.msg['To'] = receiver
        self.msg['Subject'] = subject
        try:
            self.smtp.sendmail(sender, receiver, self.msg.as_string())
        except smtplib.SMTPException as e:
            print("发信错误, 请重新登录后尝试发信!", e)
            self.statue = False
            return False
        return True

    def close_smtp(self):
        if self.smtp and self.statue:
            self.smtp.quit()


if __name__ == '__main__':
    s = SendEmail()
    s.send("python3.7 bug", "终于被我给修复了", "825662106@qq.com")
    s.close_smtp()