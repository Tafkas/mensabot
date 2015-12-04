# -*- coding: utf-8 -*-
import json
from flask import Flask, jsonify, Response, request
import random
import re
import feedparser as fp
from datetime import datetime
from lxml import etree, html

app = Flask(__name__)

colors = {'rot': 'danger', 'orange': 'warning', 'gruen': 'good'}


@app.route('/', methods=['GET'])
def hello():
    return 'Hello there'


@app.route('/lunch', methods=['GET'])
def get_lunch_location():
    loc = {'Mensa': 6, 'Golden Rice': 2, 'the other Chinese place': 1,
           'La Focaccia': 2, 'Due Fratelli': 2, 'Honigmond': 1}

    payload = {"response_type": "in_channel",
               "text": "Today\'s choice is {}".format(random.choice([k for k in loc for dummy in range(loc[k])]))
               }

    resp = Response(response=json.dumps(payload, ensure_ascii=False),
                    status=200, mimetype="application/json")
    return resp


@app.route('/mensa', methods=['GET'])
def get_mensa_food():
    f = fp.parse('http://www.studentenwerk-berlin.de/speiseplan/rss/hu_nord/tag/kurz/0')
    tree = html.fromstring(f['entries'][0]['summary'])
    food_items = tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mensa_day_speise_name", " " ))]')
    food_prices = tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mensa_day_speise_preis", " " ))]')
    food_list = [{'color': colors[x[0].xpath('./a/@href')[0].split('_')[1]],
                  'text': (re.sub('\d{2,}\w*\d*', '', x[0].text_content().strip())).rstrip() + ' '
                          + x[1].text_content().rstrip()} for x in list(zip(food_items, food_prices))]

    t = 'Today'
    if datetime.now().hour >= 16:
        t = 'Tomorrow'
        if datetime.now().weekday() == 4:
            t = 'Monday'
    payload = {"response_type": "in_channel",
               "text": '{} at Mensa'.format(t),
               'attachments': food_list}

    resp = Response(response=json.dumps(payload, ensure_ascii=False),
                    status=200, mimetype="application/json")

    return resp


if __name__ == '__main__':
    app.run()
