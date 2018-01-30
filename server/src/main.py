#=========================================================
# Package
#=========================================================
from flask import Flask
from flask_cors  import CORS
from flask_restful import Resource, Api, reqparse
import datetime
import csv

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

#=========================================================
# Custom Package
#=========================================================
import crawler

app = Flask(__name__)
api = Api(app)

"""

"""

last_updated = datetime.datetime.now().strftime('%Y-%m-%d');
isgetting = False

data = []
gernre_data = []

class Detail(Resource):
    def get(self):
        now = datetime.datetime.now()
        
        data = []

        with open('../../static/csv/detail.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        print(data)
       
        return data;

class Genre(Resource):
    def get(self):
        now = datetime.datetime.now()
        
        data = []
        
        #if last_updated is not now.strftime('%Y-%m-%d'):
        #    data = crawler.update()
        #else:
        with open('../../static/csv/detail.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        print(data)
       
        return data;
        
api.add_resource(Detail, '/')
api.add_resource(Genre, '/genre')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

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


def data_preprocess():
    """
    preprocess for speed
    - genre_data
    """
    global data
    
    data.clear()
    with open('../../static/csv/detail.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    genre_column = set()
    genre_column = list(map(lambda x: set.add(x.get('genre')), data))
    genre_column = list(zip(genre_column, [ 0 for _ in genre_column]))
    
    # TODO :: genre count 
    for item in data:
        genre_column in item.get('genre')

# TODO :: to do job 
def get_chart():
    isgetting = True
    crawler.update()
    data_preprocess()
    isgetting = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)