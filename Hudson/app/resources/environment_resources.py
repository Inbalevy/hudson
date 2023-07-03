from flask import request
from flask_restful import Resource
from hudson.models import Environment, EnvironmentActions
from hudson.models.environment import EnvironmentDestroyedError, TemplateDisabledError
from hudson.app import app
from typing import Optional
from flask_pydantic import validate

from hudson.schemas import EnvironmentSchema, ListEnvironmentSchema, EnvironmentNameSchema, CreateEnvironmentSchema

class EnvironmentResource(Resource): 
    @validate(query=EnvironmentNameSchema)  
    def get(self):
        """get a environment by name"""
        environment = EnvironmentActions.get_environment(name = request.args.get("name"))
        if environment:
            return EnvironmentSchema.from_orm(environment).dict(), 200
        return {"message": "Environment not found"}, 404

    @validate(form=CreateEnvironmentSchema)  
    def post(self):
        """create a environment by name and template_name"""
        template_name = request.form.get('template_name')
        environment_name = request.form.get('environment_name')
        try:
            environment = EnvironmentActions.create_environment(template_name, environment_name)
            return EnvironmentSchema.from_orm(environment).dict(), 201
        except Exception as e:
            return {'message': str(e)}, 500

    @validate(query=EnvironmentNameSchema) 
    def put(self):
        """update environment status"""
        environment = EnvironmentActions.get_environment(name = request.args.get("name"))
        if not environment:
            return {"message": "Environment not found"}, 404
        
        try:
            EnvironmentActions.update_environment_status(environment.id)
            return EnvironmentSchema.from_orm(environment).dict(), 200
        except EnvironmentDestroyedError as e:
            return {"message": str(e)}, 400
        


class EnvironmentsResource(Resource):   
    """list all environments"""
    @validate(query=ListEnvironmentSchema)
    def get(self):
        query_params = ListEnvironmentSchema(**request.args.to_dict()).dict(exclude_unset=True)
        environments = EnvironmentActions.list_environments(**query_params)

        environment_schemas = [EnvironmentSchema.from_orm(e) for e in environments]
        return [environment_schema.dict() for environment_schema in environment_schemas], 200