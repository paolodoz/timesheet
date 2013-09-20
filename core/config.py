import yaml
import os

# Load yaml file
core_folder = os.path.dirname(__file__)
root_folder = os.path.abspath(os.path.join(core_folder,'..'))
www_folder = os.path.abspath(os.path.join(root_folder,'www'))


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