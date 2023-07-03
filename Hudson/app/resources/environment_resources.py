from flask import request
from flask_restful import Resource
from hudson.models import Environment, EnvironmentActions
from hudson.app import app
from typing import Optional
from flask_pydantic import validate

from hudson.schemas import EnvironmentSchema, ListEnvironmentSchema, EnvironmentNameSchema

class EnvironmentResource(Resource): 
    @validate(query=EnvironmentNameSchema)  
    def get(self):
        """get a environment by name"""
        environment = EnvironmentActions.get_environment(name = request.args.get("name"))
        if environment:
            return EnvironmentSchema.from_orm(environment).dict(), 200
        return {"message": "Environment not found"}, 404

#     @validate(query=GithubUrlSchema)  
#     def post(self):
#         """create a environment by github url"""
#         github_url = request.json.get("github_url")
#         if not github_url:
#             return {"message": "GitHub URL is required"}, 400

#         environment = EnvironmentActions.create_environment(github_url, 'validate_me')
#         return EnvironmentSchema.from_orm(environment).dict(), 201

#     @validate(query=EnvironmentNameSchema) 
#     def put(self):
#         """enable a environment"""
#         environment = EnvironmentActions.get_environment(name = request.args.get("name"))
#         if not environment:
#             return {"message": "Environment not found"}, 404
        
#         if not EnvironmentActions.enable_environment(environment.id):
#             return {"message": "Environment already enabled"}, 400
        
#         return EnvironmentSchema.from_orm(environment).dict(), 200

#     @validate(query=EnvironmentNameSchema) 
#     @validate(query=EnvironmentNameSchema) 
#     def patch(self):
#         """disable a environment"""
#         environment = EnvironmentActions.get_environment(name = request.args.get("name"))
#         if not environment:
#             return {"message": "Environment not found"}, 404

#         try:
#             EnvironmentActions.disable_environment(environment.id)
#             return EnvironmentSchema.from_orm(environment).dict(), 200
#         except BadStateError as e:
#             return {"message": str(e)}, 400
#         except DependencyError as e:
#             return {"message": str(e)}, 409


class EnvironmentsResource(Resource):   
    """list all environments"""
    @validate(query=ListEnvironmentSchema)
    def get(self):
        query_params = ListEnvironmentSchema(**request.args.to_dict()).dict(exclude_unset=True)
        environments = EnvironmentActions.list_environments(**query_params)

        environment_schemas = [EnvironmentSchema.from_orm(e) for e in environments]
        return [environment_schema.dict() for environment_schema in environment_schemas], 200