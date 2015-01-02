import requests
import re
#import json
from celery import Celery
import celeryconfig

app = Celery('myapp')
app.config_from_object(celeryconfig)

#Begin Tasks

@app.task
def test_beater():
    return "I'm testing beat!"

@app.task
def check_price(item):
    data = get_page(item['url'])
    if data:
        price = parse_price(data)
        if price and price <= item["price"]:
            notify_watcher.delay(item, price)

@app.task
def notify_watcher(item, price):
    return "ALERT! One of the items you are watching has dropped in price. \n{0} now @ ${1}".format(item["name"], price)

#Begin Helper Functions

def get_page(url):
    r = requests.get(url)
    return r.text if r.ok else ""

def parse_price(data):
    match = re.search(r'<span id="priceblock_ourprice".*>\$(.*)</span>', data)
    return float(match.group(1)) if match else 0


if __name__ == '__main__':
    app.start()
