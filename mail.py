import smtplib

from email.mime.text import MIMEText

class mail:
    def __init__(self):
        return
    def send(self, sendTo, topic, message):
        msg = MIMEText(message)

        msg['Subject'] = topic
        msg['From'] = 'HackMeIfYouCanTeam@fake.com'
        msg['To'] = 'tomas930@vp.pl'
        msg['BCC'] = 'mcprogamer@gmail.com'
        s = smtplib.SMTP('localhost')
        s.sendmail('HackMeIfYouCanTeam@fake.com', sendTo, msg.as_string())
        s.quit()
