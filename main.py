import requests
from bs4 import BeautifulSoup

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

now = datetime.datetime.now()
content = ''


# extracting Hacker News Stories


def extract_news(url):
    print("Extracting Hacker News Stories...")
    cnt = ""
    cnt += f"<b>HN Top Stories: </b>\n<br>-{50}<br>"
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        cnt += ((str(i + 1) + " :: " + tag.text + "\n" + '<br> ') if tag.text != "More" else "")
    return cnt


cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += '<br> --------<br>'
content += '<br><br> End of Message'
print(content)

print("Composing Email...")

# Update Email
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = "MAIL"
TO = "mail_to"
PASSWORD = "PASSWORD"

msg = MIMEMultipart()

msg['Subject'] = f'Top News Stories HN [AUTOMATED EMAIL] {str(now.day)} - {str(now.month)} - {str(now.year)}'
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print("Initialising Server...")

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASSWORD)
server.sendmail(FROM, TO, msg.as_string())

print("Email Sent...")
server.quit()



