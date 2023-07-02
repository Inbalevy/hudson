from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

DB_URI = 'postgresql://hudsondb:HouseOfTemplates@db:5432/hudsondb'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)

def create_app():
    api = Api(app)    
    from .resources import TemplateResource, TemplatesResource
    api.add_resource(TemplateResource, '/template')
    api.add_resource(TemplatesResource, '/templates')
    return app
    

def main():
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
    
if __name__ == '__main__':
    main()
    