#=========================================================
# Package
#=========================================================
from flask import Flask
from flask_restful import Resource, Api, reqparse

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import datetime
import atexit
import csv
import time
from collections import Counter

import konlpy
#=========================================================
# Custom Package
#=========================================================
import crawler
import lyrics

app = Flask(__name__)
api = Api(app)

"""

"""

last_updated = datetime.datetime.now().strftime('%Y-%m-%d');
isgetting = False

data = []
genres = []
rank = []
words = []

class Detail(Resource):
    def get(self):
        return data
        
class Rank(Resource):
    def get(self):
        return rank
        
class Genre(Resource):
    def get(self):
        return genres
        
class WordCloud(Resource):
    def get(self):
        return words

api.add_resource(Detail, '/')
api.add_resource(Rank, '/rank')
api.add_resource(Genre, '/genre')
api.add_resource(WordCloud, '/words')

@app.after_request
def after_request(response):
    """
    For CORS.
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def data_preprocess():
    """
    preprocess for speed
    - data
    - genre_data
    """
    global data
    global rank
    global genres
    global words
    
    lyric = []
    
    data.clear()
    rank.clear()
    with open('../../static/csv/detail.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
            rank.append({
                "id":row.get('id'),
                "title":row.get('title')
            })
            lyric.append(row.get('lyric'))

    genres.clear()
    
    for key, value in Counter(map(lambda x: x.get('genre'), data)).items():
        genres.append({ 
                "genre": key.replace('&amp;','&'),
                "count": value
            })
            
    print(genres)
    
    words.clear()
    words = lyrics.get_frequency(lyric)
            
# TODO :: to do job 
def get_chart(test=False):
    """
    Crawl Melon Site.
    """
    isgetting = True
    if not test:
        crawler.update()
    data_preprocess()
    isgetting = False

"""
Register the Function to perform every hours
"""
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=get_chart,
    trigger=IntervalTrigger(hours=1),
    id='crawl_melon',
    name='Print date and time every five seconds',
    replace_existing=True)
    
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    get_chart(test=True)
    app.run(host='0.0.0.0', port=8080, debug=True)