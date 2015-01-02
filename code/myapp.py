#import requests
#import json
from celery import Celery
import celeryconfig

app = Celery('myapp')
app.config_from_object(celeryconfig)

@app.task
def test_beater():
    return "I'm testing beat!"

if __name__ == '__main__':
    app.start()
