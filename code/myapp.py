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

#Begin Helper Functions

def get_page(url):
    r = requests.get(url)
    return r.text if r.ok else ""

def parse_price(data):
    match = re.search(r'<span id="priceblock_ourprice".*>\$(.*)</span>', data)
    return float(match.group(1)) if match else 0


if __name__ == '__main__':
    app.start()
