import requests
import re
import yaml
from celery import Celery
import celeryconfig

app = Celery('myapp')
app.config_from_object(celeryconfig)

#Begin Tasks

@app.task
def test_beater():
    return "I'm testing beat!"

@app.task
def queue_price_checks():
    try:
        stream = open("watch.yml", "r")
    except IOError:
        print "error opening watch.yml"

    data = yaml.load(stream)[0]

    if data:
        for item in data["watch"]:
            item.update({"email": data["email"]})
            check_price.delay(item)

@app.task
def check_price(item):
    data = get_page(item['url'])
    if data:
        price = parse_price(data)
        if price and price <= item["price"]:
            notify_watcher.delay(item, price)
        else:
            return "nothing to report here - {0} @ $ {1}".format(item["name"], price)

@app.task
def notify_watcher(item, price):
    return "ALERT! One of the items you are watching has dropped in price. \n{0} now @ ${1}".format(item["name"], price)

#Begin Helper Functions

def get_page(url):
    r = requests.get(url)
    return r.text if r.ok else ""

def parse_price(data):
    match = re.search(r'<span id="priceblock_ourprice".*>(.*)</span>', data)
    p = re.sub(r'[^\d.]', '', match.group(1))
    return float(p) if match else 0


if __name__ == '__main__':
    app.start()
