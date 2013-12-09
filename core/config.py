import yaml, os, sys
from mako.lookup import TemplateLookup

version = '0.1'

# Define common paths based on current file position
core_folder = os.path.dirname(__file__)
schemas_folder = os.path.abspath(os.path.join(core_folder,'schemas'))
root_folder = os.path.abspath(os.path.join(core_folder,'..'))
www_folder = os.path.abspath(os.path.join(root_folder,'www'))
templates_folder = os.path.abspath(os.path.join(www_folder,'templates'))
views_folder = os.path.abspath(os.path.join(www_folder,'views'))
notifications_folder = os.path.abspath(os.sep.join((core_folder,'notifications/mails')))

# Set template engines
templates = TemplateLookup(directories=[templates_folder])
views = TemplateLookup(directories=[views_folder])
notifications = TemplateLookup(directories=[notifications_folder])

# Load database schema validation from database.yaml
schema_path = os.path.join(schemas_folder, 'database.yaml')
schema = yaml.load(file(schema_path, 'r'))
collections = schema.keys()

# Load permissions schema from permissions.yaml
permissions_path = os.path.join(schemas_folder, 'permissions.yaml')
restrictions_schema = yaml.load(file(permissions_path, 'r'))

# Load requests schema from requests.yaml
requests_schema_path = os.path.join(schemas_folder, 'requests.yaml')
requests_schema = yaml.load(file(requests_schema_path, 'r'))

# Load views restrictions schema from views_restrictions.yaml
views_restrictions_schema_path = os.path.join(schemas_folder, 'views.yaml')
views_restrictions_schema = yaml.load(file(views_restrictions_schema_path, 'r'))

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
conf_uploads = conf['uploads']
conf_reports = conf['reports']
conf_notifications = conf['notifications']

conf_approval_flow = conf['approval_flow']
conf_approved = 0

# Create configurations folders if do not exist
paths =  [ conf_session['tools.sessions.storage_path'], conf_uploads['folder'] ]

# Installation path
installation_path = os.path.realpath(os.path.join(os.path.dirname(__file__),'..'))

for path in paths:

    if not os.path.isabs(path):
        path = os.path.join(installation_path,path) 

    if not os.path.isdir(path):
        # TODO: check also folder permissions
        try:
            os.mkdir(path, 0770)
        except Exception as e:
            sys.exit('Can\'t create folder \'%s\'' % (path))
