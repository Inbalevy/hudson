from flask import request
from flask_restful import Resource
from hudson.models import Template, TemplateActions
from hudson.app.app import app
from flask_pydantic import validate

# template_schema = Template()

class TemplateResource(Resource):   
    @validate
    def get(self, name: str):
        """get a template by name"""
        template = TemplateActions.get_template(name = name)
        if template:
            return template, 200
        return {"message": "Template not found"}, 404

    def post(self):
        """create a template by github url"""
        github_url = request.json.get("github_url")
        if not github_url:
            return {"message": "GitHub URL is required"}, 400

        template = Template.create_template(github_url)
        return template, 201

    def put(self, name):
        """enable a template"""
        template = Template.get_template(name = name)
        if not template:
            return {"message": "Template not found"}, 404

        template.enable_template()
        return template, 200

    def patch(self, name):
        """disable a template"""
        template = Template.get_template(name = name)
        if not template:
            return {"message": "Template not found"}, 404

        template.disable_template()
        return template, 200

    def delete(self, name):
        """remove a template"""
        template = Template.get_template(name = name)
        if not template:
            return {"message": "Template not found"}, 404

        template.delete_template()
        return {"message": "Template deleted"}, 200


class TemplatesResource(Resource):   
    def get(self):
        templates = TemplateActions.list_templates()
        return templates, 200