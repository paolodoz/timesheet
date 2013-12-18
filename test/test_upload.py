from testclasses import TestClassBase, CookieJar, admin_data
import itertools
import mimetools
import mimetypes
from cStringIO import StringIO
import urllib, urllib2, os, stat, json

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

doseq = 1

class MultipartPostHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order - 10 # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for(key, value) in data.items():
                     if type(value) == file:
                         v_files.append((key, value))
                     else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", traceback

            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)

                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if(request.has_header('Content-Type')
                   and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print "Replacing %s with %s" % (request.get_header('content-type'), 'multipart/form-data')
                request.add_unredirected_header('Content-Type', contenttype)

            request.add_data(data)
        
        return request

    def multipart_encode(vars, files, boundary = None, buf = None):
        if boundary is None:
            boundary = mimetools.choose_boundary()
        if buf is None:
            buf = StringIO()
        for(key, value) in vars:
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"' % key)
            buf.write('\r\n\r\n' + value + '\r\n')
        for(key, fd) in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = fd.name.split('/')[-1]
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename))
            buf.write('Content-Type: %s\r\n' % contenttype)
            # buffer += 'Content-Length: %s\r\n' % file_size
            fd.seek(0)
            buf.write('\r\n' + fd.read() + '\r\n')
        buf.write('--' + boundary + '--\r\n\r\n')
        buf = buf.getvalue()
        return boundary, buf
    multipart_encode = Callable(multipart_encode)

    https_request = http_request



class Upload(TestClassBase):
    
    def setUp(self):

        self.execOnTearDown = []
        self.cookies = CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies), MultipartPostHandler())
        self._assert_unlogged()
        self.admin_data = admin_data
        self._login(admin_data[0], 'administrator')
        self._assert_logged(admin_data[0])
        
    
    def _assert_upload(self, filepath):
        json_upload = json.loads(self.opener.open('https://localhost:9090/file/upload', { 'data': open(filepath, 'rb') }, timeout=36000).read())
        
        self.assertEqual(json_upload.keys(), ['upload_id', 'error'])
        self.assertIsNone(json_upload['error'])
        
        return json_upload
    
    def _assert_download(self, upload_id, localfilepath):
        
        data_download = self.opener.open('https://localhost:9090/file/download', { 'upload_id' : upload_id  }, timeout=36000).read()

        if localfilepath:
            data_local = open(localfilepath, 'rb').read()
        else:
            data_local = ''
        
        self.assertEqual(data_download, data_local)
        
    
    def test_text(self):
        json_upload = self._assert_upload('/etc/protocols')
        self._assert_download(json_upload['upload_id'], '/etc/protocols')
        
        self._assert_req('/file/remove', [ json_upload['upload_id'] ] , { 'error' : None })
        self._assert_download(json_upload['upload_id'], '')
        
        
    def test_binary(self):
        json_upload = self._assert_upload('/usr/bin/yes')
        self._assert_download(json_upload['upload_id'], '/usr/bin/yes')
        
        # Delete
        self.execOnTearDown.append(('/file/remove', [ json_upload['upload_id'] ] , { 'error' : None }))
        
    def test_big_binary(self):
        json_upload = self._assert_upload('/bin/bash')
        self._assert_download(json_upload['upload_id'], '/bin/bash')
        
        # Delete
        self.execOnTearDown.append(('/file/remove', [ json_upload['upload_id'] ] , { 'error' : None }))
            
