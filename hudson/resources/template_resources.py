from flask import request
from flask_restful import Resource
from hudson.models import Template, TemplateActions
from hudson.models.template import TemplateDisabledError, DependencyError
from flask_pydantic import validate

from hudson.schemas import TemplateSchema, ListTemplatesSchema, TemplatesNameSchema, GithubUrlSchema

class TemplateResource(Resource): 
    @validate(query=TemplatesNameSchema)  
    def get(self):
        """get a template by name"""
        template = TemplateActions.get_template(name = request.args.get("name"))
        if template:
            return TemplateSchema.from_orm(template).dict(), 200
        return {"message": "Template not found"}, 404

    @validate(query=GithubUrlSchema)  
    def post(self):
        """create a template by github url"""
        github_url = request.json.get("github_url")
        if not github_url:
            return {"message": "GitHub URL is required"}, 400

        template = TemplateActions.create_template(github_url, 'validate_me')
        return TemplateSchema.from_orm(template).dict(), 201

    @validate(query=TemplatesNameSchema) 
    def put(self):
        """enable a template"""
        template = TemplateActions.get_template(name = request.args.get("name"))
        if not template:
            return {"message": "Template not found"}, 404
        
        if not TemplateActions.enable_template(template.id):
            return {"message": "Template already enabled"}, 400
        
        return TemplateSchema.from_orm(template).dict(), 200

    @validate(query=TemplatesNameSchema) 
    def patch(self):
        """disable a template"""
        template = TemplateActions.get_template(name = request.args.get("name"))
        if not template:
            return {"message": "Template not found"}, 404

        try:
            TemplateActions.disable_template(template.id)
            return TemplateSchema.from_orm(template).dict(), 200
        except TemplateDisabledError as e:
            return {"message": str(e)}, 400
        except DependencyError as e:
            return {"message": str(e)}, 409


    @validate(query=TemplatesNameSchema) 
    def delete(self):
        """remove a template"""
        template = Template.get_template(name = request.args.get("name"))
        if not template:
            return {"message": "Template not found"}, 404


class TemplatesResource(Resource):   
    """list all templates"""
    @validate(query=ListTemplatesSchema)
    def get(self):
        templates = TemplateActions.list_templates(only_enabled=request.args.get("only_enabled"))
        template_schemas = [TemplateSchema.from_orm(t) for t in templates]
        return [template_schema.dict() for template_schema in template_schemas], 200
