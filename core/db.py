try:
    from pymongo import MongoClient as Connection
except ImportError, e:
    from pymongo import Connection

from core.config import collections, conf_mongodb, conf_auth

connection = Connection(conf_mongodb['hostname'], conf_mongodb['port'])
db = connection[conf_mongodb['db']]

# Create on database missing collections names
for missing_collection in (set(collections) - set(db.collection_names())):
    db[missing_collection]
    
# Create default admin user, is in conf and not already set
# if conf_auth['admin.default.enabled'] and db['users'].findOne({ '_id' : 0 }):
#     db['users'].insert( { '_id' : 0, 'name' : 'Admin', 'surname' : 'Default', 'email' : 'admin@localhost', 'phone' : '', 'mobile' : '', 'city' : '', 'role' : 'administrator' })