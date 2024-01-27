import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
load_dotenv()
import os
MAIL_HOST = os.getenv('MAIL_HOST',"")
MAIL_USER = os.getenv('MAIL_USER',"")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD","")
SENDER = os.getenv("SENDER","")
#print(MAIL_HOST,MAIL_USER,MAIL_PASSWORD,SENDER)
#设置服务器所需信息
#163邮箱服务器地址
class SendEmail:
    def __init__(self):
        self.description = "<send email>: to use this tool you need know the address of the receiver, and the message you want to send"
        self.jsonloadF = """
        {
            "message": "the message to send",
            "address": "the address of the receiver",
        }
        """
    def description(self):
        return self.description
    def jsonload(self):
        return self.json
    def jsonrun(self,json):
        message = json['message']
        address = json['address']
        return SendEmail.run(message,address)
    @staticmethod
    def run(message,address): 
        mail_host = MAIL_HOST 
        #163用户名
        mail_user = MAIL_USER
        #密码(部分邮箱为授权码) 
        mail_pass = MAIL_PASSWORD
        #邮件发送方邮箱地址
        sender = SENDER
        #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = [address]  

        #设置email信息
        #邮件内容设置
        message = MIMEText(message,'plain','utf-8')
        #邮件主题       
        message['Subject'] = 'EVA'  # 可以在这个地方改你的邮件主题 
        #发送方信息
        message['From'] = sender 
        #接受方信息     
        message['To'] = receivers[0]  

        #登录并发送邮件
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host)
            #登录到服务器
            smtpObj.login(mail_user,mail_pass) 
            #发送
            smtpObj.sendmail(
                sender,receivers,message.as_string()) 
            #退出
            smtpObj.quit() 
            return "send email successfully"
        except smtplib.SMTPException as e:
            #print('error',e) #打印错误
            return f"send email failed because of the ￥￥{e}￥￥"
if __name__ == '__main__':
    jsonEVA = {
        "message": "Good Evening",
        "address": "2539906978@qq.com",
    }
    sendemail = SendEmail()
    print(sendemail.jsonrun(jsonEVA))
