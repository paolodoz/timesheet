import tempfile, os, shutil, cherrypy, time
from core.config import conf_uploads
from core.db import db
from core.validation import TSValidationError, validate_request, cgi, ObjectId
from core.permissions import check_action_permissions

def upload():
    
    # Check permissions  
    check_action_permissions('insert', 'file')
    validate_request('file_upload', cherrypy.request.params)
    
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
        
        uploaded_temp_path = os.path.join(conf_uploads['folder'], uploaded_temp.name)
        uploaded_path = os.path.join(conf_uploads['folder'], upload_id)
        
        os.rename(uploaded_temp_path, uploaded_path)

    except Exception as e:
        raise
    
    return upload_id


def download(upload_id):
    
    # Check permissions  
    check_action_permissions('get', 'file')
    validate_request('file_download', cherrypy.request.params)
    
    upload_id = ObjectId(upload_id)
    
    json_found = db.upload.find_one({ '_id' : upload_id }, { 'content_type' : 1})
    file_path = os.path.abspath(os.path.join(conf_uploads['folder'], str(upload_id)))
    
    if not json_found:
        raise TSValidationError("File id not found")
    
    return file_path, json_found['content_type']
