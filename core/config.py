import yaml, os
from mako.lookup import TemplateLookup

version = '0.1'

# Define common paths based on current file position
core_folder = os.path.dirname(__file__)
root_folder = os.path.abspath(os.path.join(core_folder,'..'))
www_folder = os.path.abspath(os.path.join(root_folder,'www'))
templates_folder = os.path.abspath(os.path.join(www_folder,'templates'))
views_folder = os.path.abspath(os.path.join(www_folder,'views'))

# Set template engine
templates = TemplateLookup(directories=[templates_folder])

# Load database schema validation from schema.yaml
schema_path = os.path.join(core_folder, 'schema.yaml')
schema = yaml.load(file(schema_path, 'r'))
collections = schema.keys()

# Load permissions schema from permissions.yaml
permissions_path = os.path.join(core_folder, 'permissions.yaml')
restrictions_schema = yaml.load(file(permissions_path, 'r'))

# Load requests schema from requests.yaml
datamine_path = os.path.join(core_folder, 'datamine.yaml')
datamine_schema = yaml.load(file(datamine_path, 'r'))

# Load configuration from config.yaml
conf_path = os.path.join(core_folder, 'config.yaml')
conf = yaml.load(file(conf_path, 'r'))

# Adding static root dir absolute path
conf['static']['/'] = {}
conf['static']['/']['tools.staticdir.root'] = root_folder

# Save conf as accessible dicts
conf_server = conf['server']
conf_static = conf['static']
conf_session = conf['session']
conf_auth = conf['auth']
conf_auth_db = conf['auth_db']
conf_auth_ldap = conf['auth_ldap']
conf_mongodb = conf['mongodb']
conf_logging = conf['logging']