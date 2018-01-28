#=========================================================
# Package
#=========================================================
from flask import Flask
from flask_cors  import CORS
from flask_restful import Resource, Api, reqparse
import datetime
import csv

#=========================================================
# Custom Package
#=========================================================
import crawler

app = Flask(__name__)
api = Api(app)

"""

"""

last_updated = datetime.datetime.now().strftime('%Y-%m-%d');

class Detail(Resource):
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

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)