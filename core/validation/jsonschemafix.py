from core.config import schemas_folder
from jsonschema.validators import Draft4Validator, create
import json, os

"""
Create personal validator to avoid annoying error while validating 
jsonschema raised in case of empty enum lists in permissions.yaml 
schema. 
"""

jsonschema_draft_path = os.path.join(schemas_folder, 'draft4fix.json')
schema = json.load(open(jsonschema_draft_path,'r')) 
validator = create(schema, Draft4Validator.VALIDATORS, version="fixed4")
