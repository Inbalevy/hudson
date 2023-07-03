from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from hudson.database import db

DB_URI = 'postgresql://hudsondb:HouseOfTemplates@db:5432/hudsondb'


def add_resources(api):
    from hudson.resources import EnvironmentResource, EnvironmentsResource, TemplateResource, TemplatesResource
    api.add_resource(TemplateResource, '/template')
    api.add_resource(TemplatesResource, '/templates')
    api.add_resource(EnvironmentResource, '/environment')
    api.add_resource(EnvironmentsResource, '/environments')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    db.init_app(app)
    api = Api(app)  
    add_resources(api)
    return app
    

def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        
    app.run(host='0.0.0.0', port=5000, debug=True)
    
if __name__ == '__main__':
    main()
    