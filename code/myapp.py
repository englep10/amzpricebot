import requests
import smtplib
import re
from celery import Celery
import celeryconfig
from settings import account, app_pwd, watch_list

app = Celery('myapp')
app.config_from_object(celeryconfig)

#Begin Tasks

@app.task
def test_beater():
    return "I'm testing beat!"

@app.task
def queue_price_checks():
    data = watch_list

    for count, item in enumerate(data):
        delay = count * 5
        check_price.apply_async(args=[item], countdown=delay)

@app.task
def check_price(item):
    data = get_page(item['url'])
    if data:
        price = parse_price(data)
        if price and price <= item["price"]:
            notify_watcher.delay(item, price)
        else:
            return "nothing to report here - {0} @ $ {1}".format(item["name"], price)
    else:
        raise check_price.retry(args=[item], countdown=10)

@app.task
def notify_watcher(item, price):
    msg = "ALERT! One of the items you are watching has dropped in price. \n{0} now @ ${1}".format(item["name"], price)
    send_email(msg)
    return msg

#Begin Helper Functions

def get_page(url):
    r = requests.get(url)
    return r.text if r.ok else ""

def parse_price(data):
    match = re.search(r'<span id="priceblock_ourprice".*>(.*)</span>', data)
    p = re.sub(r'[^\d.]', '', match.group(1))
    return float(p) if match else 0

def send_email(content):
    """
    Sends email
    :param content: content of the email to be sent
    """

    gmail_u = account
    gmail_p = app_pwd
    subject = "AMAZON Price BOT Alert"
    target = account
    body = content

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.login(gmail_u, gmail_p)

    headers = ["from: " + gmail_u,
               "subject: " + subject,
               "to: " + target,
               "mime-version: 1.0",
               "content-type: text/html"]

    headers = "\r\n".join(headers)
    session.sendmail(gmail_u, target, headers + "\r\n\r\n" + body)
    session.quit()

if __name__ == '__main__':
    app.start()
