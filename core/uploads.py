import tempfile, os, shutil
from core.config import conf_uploads
from core.db import db



def upload(file_uploading):    
    
    uploaded_temp = tempfile.NamedTemporaryFile(dir=conf_uploads['folder'])

    try:
        while True:
            data = file_uploading.file.read(8192)
            if not data:
                break
            uploaded_temp.write(data)
    
        uploaded_temp.flush()
        file_id = str(db.upload.insert({ 'name' : str(file_uploading.name), 'content_type' : str(file_uploading.content_type) }))
        
        uploaded_temp_path = os.path.join(conf_uploads['folder'], uploaded_temp.name)
        uploaded_path = os.path.join(conf_uploads['folder'], file_id)
        
        shutil.copyfile(uploaded_temp_path, uploaded_path)

    except Exception as e:
        raise
    
    return file_id