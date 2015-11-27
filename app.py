from flask import Flask, jsonify
import re
import feedparser as fp
from lxml import etree, html

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return 'Hello there'


@app.route('/mensa', methods=['GET'])
def get_mensa_food():
    f = fp.parse('http://www.studentenwerk-berlin.de/speiseplan/rss/hu_nord/tag/kurz/0')
    tree = html.fromstring(f['entries'][0]['summary'])
    food_items = tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mensa_day_speise_name", " " ))]')
    food_list = [re.sub('\d{2,}\w*\d*', '', x.text_content().strip()) for x in food_items]
    r = ''
    for food_item in food_list:
        r += food_item + '<\n>'
    payload = {"text": 'Today at Mensa',
               'attachments': {'text': r}}
    return jsonify(payload)


if __name__ == '__main__':
    app.run()
