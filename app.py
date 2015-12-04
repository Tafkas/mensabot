# -*- coding: utf-8 -*-
import json
from flask import Flask, jsonify, Response, request
import re
import feedparser as fp
from lxml import etree, html

app = Flask(__name__)

colors = {'rot': 'danger', 'orange': 'warning', 'gruen': 'good'}


@app.route('/', methods=['GET'])
def hello():
    return 'Hello there'


@app.route('/mensa', methods=['GET'])
def get_mensa_food():
    f = fp.parse('http://www.studentenwerk-berlin.de/speiseplan/rss/hu_nord/tag/kurz/0')
    tree = html.fromstring(f['entries'][0]['summary'])
    food_items = tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mensa_day_speise_name", " " ))]')
    food_prices = tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mensa_day_speise_preis", " " ))]')
    food_list = [{'color': colors[x[0].xpath('./a/@href')[0].split('_')[1]],
                  'text': (re.sub('\d{2,}\w*\d*', '', x[0].text_content().strip())).rstrip() + ' '
                          + x[1].text_content().rstrip()} for x in list(zip(food_items, food_prices))]

    payload = {"text": 'Today at Mensa',
               'attachments': food_list}

    resp = Response(response=json.dumps(payload, ensure_ascii=False),
                    status=200, mimetype="application/json")

    return resp


if __name__ == '__main__':
    app.run()
