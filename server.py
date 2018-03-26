
import sys

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from shutil import copy2
import cgi
import os
import subprocess
import tempfile
import zipfile
import uuid

import mimetypes as memetypes
import shutil


PORT = int(sys.argv[1])


class StoreHandler(BaseHTTPRequestHandler):

    def dump_syms(self):
        SESSIONID = str(uuid.uuid4())

        print "Processing session %s" % SESSIONID

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        # Help func
        def createDirIfNotExist(path):
            if not os.path.exists(path):
                os.makedirs(path)

        def zipdir(path, ziph, dir_startwith):
            # ziph is zipfile handle
            for root, dirs, files in os.walk(path):
                for file in files:
                    fpath = os.path.join(root, file)

                    if fpath.startswith(dir_startwith):
                        ziph.write(fpath, fpath[len(dir_startwith):])
                    else:
                        ziph.write(fpath)

        # Here we will store all data including generated symbols
        session_dir = os.path.join(tempfile.gettempdir(), SESSIONID)
        createDirIfNotExist(session_dir)

        # Symbols dir
        symbols_out_dir = os.path.join(session_dir, 'symbols')
        createDirIfNotExist(symbols_out_dir)

        # .so files
        libs_dir = os.path.join(session_dir, 'libs')
        createDirIfNotExist(libs_dir)

        # Save input date
        input_file = os.path.join(session_dir, form['file'].disposition_options['filename'])
        data = form['file'].file.read()
        open(input_file, "wb").write(data)

        # Locate input data insise libs dir
        if input_file.endswith(".zip"):
            zip_ref = zipfile.ZipFile(input_file, 'r')
            zip_ref.extractall(libs_dir)
            zip_ref.close()
        else:
            copy2(input_file, libs_dir)

        # Run dump_syms
        for root, subdirs, files in os.walk(libs_dir):   # Recursively listdir
            for file in files:
                if file.endswith(".so"):
                    lib_fullpath = os.path.join(root, file)
                    print "processing: ", lib_fullpath

                    # Create symbols
                    symbol_out_file = os.path.join(symbols_out_dir, '%s.sym' % file)
                    with open(symbol_out_file, 'w') as out:
                        subprocess.call(['dump_syms', lib_fullpath], stdout=out)

                    # Create structure
                    with open(symbol_out_file, 'r') as f:
                        first_line = f.readline().strip()
                        line = first_line.split(' ')
                        try:
                            syms_path = os.path.join(symbols_out_dir, line[-1], line[3])
                            try:
                                os.makedirs(syms_path)
                            except OSError:
                                pass
                        except:
                            syms_path = None

                    if syms_path is not None:
                        copy2(symbol_out_file, syms_path)

                    os.remove(symbol_out_file)

        zip_out = os.path.join(session_dir, "result.zip")
        zipf = zipfile.ZipFile(zip_out, 'w', zipfile.ZIP_DEFLATED)
        zipdir(symbols_out_dir, zipf, session_dir)
        zipf.close()

        self.respond_file(zip_out)

    def do_POST(self):
        if self.path == '/dump_syms':
            self.dump_syms()
        elif self.path == '/minidump_stackwalk':
            self.minidump_stackwalk()

        self.respond('cannot find endpoint')

    def respond(self, response, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response)

    def respond_file(self, file_path):
        content, encoding = memetypes.MimeTypes().guess_type(file_path)
        if content is None:
            content = "application/octet-stream"

        info = os.stat(file_path)

        self.send_response(200)
        self.send_header("Content-Type", content)
        self.send_header("Content-Encoding", encoding)
        self.send_header("Content-Length", info.st_size)
        self.end_headers()

        f = open(file_path, 'rb')
        shutil.copyfileobj(f, self.wfile)
        f.close()

        return file_path


try:
    server = HTTPServer(('', PORT), StoreHandler)
    print 'Started httpserver on port ', PORT

    server.serve_forever()
except KeyboardInterrupt:
    print '^C received, shutting down the web server'
server.socket.close()
