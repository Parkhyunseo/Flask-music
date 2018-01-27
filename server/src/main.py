from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class CreateUser(Resource):
    def post(self):
        try:
            
            return {'status': 'success'}
        except Exception as e:
            return {'error':str(e)};
        
api.add_resource(CreateUser, '/user')

if __name__ == '__main__':
    app.run(debug=True)