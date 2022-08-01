import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart()
msg['From'] = 'investmentsimulator@yandex.ru'
msg['To'] = 'you@gmail.com'
msg['Subject'] = 'Test e-mail send'
message = 'Test e-mail send'
msg.attach(MIMEText(message))
def e_mailsend():
    mailserver = smtplib.SMTP_SSL('smtp.yandex.com',465)
    mailserver.ehlo()
    mailserver.ehlo()
    mailserver.login('investmentsimulator@yandex.ru', 'tiefsgvtcfkwdeos')
    mailserver.sendmail('investmentsimulator@yandex.ru',email ,msg.as_string())
    mailserver.quit()
