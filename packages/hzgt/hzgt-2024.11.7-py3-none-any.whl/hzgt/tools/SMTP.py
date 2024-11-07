# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Union

class Smtpop:
    """
    基于SMTPLib库封装, 提供SMTP邮件发送功能
    """

    def __init__(self, smtp_server: str, port: int, username: str, password: str):
        """
        初始化SMTP客户端

        :param smtp_server: SMTP服务器地址 例如: "smtp.qq.com"
        :param port: SMTP服务器端口 例如: 587
        :param username: 登录用户名
        :param password: 授权码
        """
        self.smtp_server = smtp_server
        self.port = int(port)
        self.username = username
        self.password = password
        self.server = None
        self.recipients = []
        self.msg = MIMEMultipart()

    def __enter__(self):
        """
        上下文管理器进入方法, 登录SMTP服务器
        """
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        上下文管理器退出方法, 关闭SMTP连接
        """
        self.close()

    def login(self):
        """
        登录SMTP服务器
        """
        self.server = smtplib.SMTP(self.smtp_server, self.port)
        self.server.starttls()  # 启用TLS加密
        self.server.login(self.username, self.password)

    def add_recipient(self, recipient: Union[str, list, tuple, set], *args):
        """
        添加收件人

        :param recipient: 收件人邮箱地址
        :type recipient: Union[str, list, tuple, set]

        :param args: *args也能接受单个的收件人邮箱地址或者可迭代的收件人邮箱地址容器(如列表、元组、集合)
        """
        if isinstance(recipient, str):
            self.recipients.append(recipient)
        elif isinstance(recipient, list) or isinstance(recipient, tuple) or isinstance(recipient, set):
            for rs in recipient:
                self.recipients.append(rs)

        for arg in args:
            if isinstance(arg, str):
                self.recipients.append(arg)
            elif isinstance(arg, list) or isinstance(arg, tuple) or isinstance(arg, set):
                for item in arg:
                    self.recipients.append(item)

    def add_file(self, file_path: str):
        """
        添加附件到邮件中

        :param file_path: 附件文件路径
        """
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={file_path}")
            self.msg.attach(part)

    def send_email(self, subject: str, body: str, html=False):
        """
        发送邮件

        :param subject: 邮件主题
        :param body: 邮件正文
        :param html: 布尔值, 指示邮件正文是否为HTML格式默认为False
        """
        self.msg["From"] = self.username
        self.msg["To"] = ", ".join(self.recipients)
        self.msg["Subject"] = subject

        if html:
            self.msg.attach(MIMEText(body, "html"))
        else:
            self.msg.attach(MIMEText(body, "plain"))

        # 发送邮件
        self.server.sendmail(self.username, self.recipients, self.msg.as_string())

    def close(self):
        """
        关闭SMTP连接
        """
        if self.server:
            self.server.quit()


