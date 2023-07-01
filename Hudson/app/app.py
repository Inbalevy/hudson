from flask import Flask
from flask_restful import Api
from .resources import TemplateResource

app = Flask(__name__)
api = Api(app)

api.add_resource(TemplateResource, '/templates')

def main():
    app.run(debug=True)
    
    
if __name__ == '__main__':
    main()
    