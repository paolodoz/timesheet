import tempfile, os, shutil, cherrypy, time
from core.config import conf_uploads
from core.api.crud import db
from core.validation.validation import TSValidationError, validate_request, cgi, ObjectId, sanitize_objectify_json
from core.validation.permissions import check_datamine_permissions
import logging

db_log_severity = logging.INFO

def upload():
    
    # Check permissions  
    check_datamine_permissions('file_upload', cherrypy.request.params)
    
    file_uploading = cherrypy.request.params['data']
    
    uploaded_temp = tempfile.NamedTemporaryFile(mode='w+b', dir=conf_uploads['folder'], delete=False)

    try:
        while True:
            data = file_uploading.file.read(8192)
            if not data:
                break
            else:
                uploaded_temp.write(data)
    
        uploaded_temp.close()
        upload_id = str(db.upload.insert({ 'name' : str(file_uploading.filename), 'content_type' : cgi.escape(str(file_uploading.content_type)), 'owner' : cherrypy.session['_ts_user']['username'], 'date' :  time.strftime("%Y-%m-%d%H:%M:%S", time.gmtime()) }))

        cherrypy.log('%s %s' % (str(file_uploading.filename), str(file_uploading.content_type)) , context = 'TS.FILE.UPLOAD', severity = db_log_severity)
        
        uploaded_temp_path = os.path.join(conf_uploads['folder'], uploaded_temp.name)
        uploaded_path = os.path.join(conf_uploads['folder'], upload_id)
        
        os.rename(uploaded_temp_path, uploaded_path)

    except Exception as e:
        raise
    
    return upload_id


def download(upload_id):
    
    # Check permissions  
    check_datamine_permissions('file_download', cherrypy.request.params)
    
    upload_id = ObjectId(upload_id)
    
    json_found = db.upload.find_one({ '_id' : upload_id }, { 'content_type' : 1})
    file_path = os.path.abspath(os.path.join(conf_uploads['folder'], str(upload_id)))
    
    cherrypy.log('%s' % (upload_id), context = 'TS.FILE.DOWNLOAD.upload_id', severity = db_log_severity)
    
    if not json_found:
        raise TSValidationError("File id not found")
    
    return file_path, json_found['content_type']


def remove(upload_ids):

    check_datamine_permissions('file_remove', cherrypy.request.params)
    
    # Sanify upload_id (to match with sanified documents)
    # TODO: check why does not objectify lists
    #upload_ids = sanitize_objectify_json(upload_ids)
    
    cherrypy.log('%s' % (str(upload_ids)), context = 'TS.FILE.REMOVE.upload_ids', severity = db_log_severity)
    
    # Requests
    for upload_id in upload_ids:
        
        db.upload.remove({ '_id' : ObjectId(upload_id) })
        
        file_path = os.path.abspath(os.path.join(conf_uploads['folder'], str(upload_id)))
        
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except:
                pass
            else:
                continue
            
        cherrypy.log('Error removing file \'%s\'' % (file_path), context = 'TS.FILE.REMOVE.file_path', severity = db_log_severity)
            
