import requests
import datetime
import smtplib
import time
import schedule

from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from secrets import secrets

now = datetime.datetime.now()

content = ''

def extract_news(url):
    print('Extracting Page Six News....')
    cnt = ''
    cnt += f'<b>Page Six Top Stories:</b><br>{"-"*50}<br>'
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('div', attrs = {'class' : 'story__text'})):
        if tag.a:
            cnt += f"<b>{str(i)}</b> :: {tag.a.text.lstrip().rstrip().replace('  ', '')} <a href={tag.a['href']}>(Get the tea!)</a><br>"
    return cnt

cnt = extract_news('https://pagesix.com/celebrity-news/')
content += cnt

print("Composing Email....")

SERVER = secrets.get("SERVER")
PORT = secrets.get("PORT")
FROM = secrets.get("FROM")
TO = secrets.get("TO")
PASS = secrets.get("PASS")

msg = MIMEMultipart()
msg['Subject'] = f'Top News Stories Page Six [Automated Email] {str(now.month)}-{str(now.day)}-{str(now.year)}'
msg['From'] = FROM
msg['To'] = ", ".join(TO)
msg.attach(MIMEText(content, 'html'))

print("Initializing Server...")

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(0)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print("Email Sent!")
server.quit()

