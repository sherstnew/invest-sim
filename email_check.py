import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
email = "Frolova-Helen@yandex.ru"
msg = MIMEMultipart()
msg['From'] = 'investmentsimulator@yandex.ru'
msg['To'] = email
msg['Subject'] = 'Test e-mail send'
message = 'Test e-mail send'
msg.attach(MIMEText(message))
mailserver = smtplib.SMTP_SSL('smtp.yandex.com',465)
mailserver.ehlo()
mailserver.ehlo()
mailserver.login('investmentsimulator@yandex.ru', 'tiefsgvtcfkwdeos')
mailserver.sendmail('investmentsimulator@yandex.ru',email ,msg.as_string())
mailserver.quit()
