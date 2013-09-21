import yaml
import os


# Define common paths based on current file position
core_folder = os.path.dirname(__file__)
root_folder = os.path.abspath(os.path.join(core_folder,'..'))
www_folder = os.path.abspath(os.path.join(root_folder,'www'))
templates_folder = os.path.abspath(os.path.join(www_folder,'templates'))
views_folder = os.path.abspath(os.path.join(www_folder,'views'))

# Load yaml file
yaml_path = os.path.join(core_folder, 'config.yaml')
conf = yaml.load(file(yaml_path, 'r'))

# Adding static root dir absolute path
conf['static']['/'] = {}
conf['static']['/']['tools.staticdir.root'] = root_folder
# conf['static']['tools.staticdir.dir'] = os.path.abspath(path.join())

# Save it as accessible dicts
conf_server = conf['server']
conf_static = conf['static']
conf_auth = conf['auth']