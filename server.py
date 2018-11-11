import sys

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from shutil import copy2
import cgi
import os
import subprocess
import tempfile
import zipfile
import uuid
from subprocess import Popen, PIPE
import mimetypes as memetypes
import shutil

PORT = int(sys.argv[1])


def zipdir(path, ziph, dir_startwith):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            fpath = os.path.join(root, file)

            if fpath.startswith(dir_startwith):
                ziph.write(fpath, fpath[len(dir_startwith):])
            else:
                ziph.write(fpath)


# Help func
def createDirIfNotExist(path):
    if not os.path.exists(path):
        os.makedirs(path)


class StoreHandler(BaseHTTPRequestHandler):
    def minidump_stackwalk(self, form):
        session_dir = self.generateSessionDir()

        symbols_zip_file = self.save_file(session_dir, form, 'symbols')
        dump_file = self.save_file(session_dir, form, 'dump')

        # .so files
        symbols_dir = os.path.join(session_dir, 'symbols')
        createDirIfNotExist(symbols_dir)

        # Locate input data insise libs dir
        if symbols_zip_file.endswith(".zip"):
            zip_ref = zipfile.ZipFile(symbols_zip_file, 'r')
            zip_ref.extractall(symbols_dir)
            zip_ref.close()

            # try to find a folder with symbols
            while len(filter(lambda f: f.endswith(".so"), os.listdir(symbols_dir))) == 0:
                symbols_dir = os.path.join(symbols_dir, os.listdir(symbols_dir)[0])

            print("SymbolsDir %s, SymbolsDirectories %s", symbols_dir, os.listdir(symbols_dir))

        else:
            self.respond("Symbols need to be a zip file", 400)
            shutil.rmtree(session_dir)
            return
        try:
            p = Popen(['minidump_stackwalk', dump_file, symbols_dir], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, error = p.communicate()
            if p.returncode != 0:
                self.respond("minidump_stackwalk failed %d %s %s" % (p.returncode, output, error), 500)
            else:
                self.respond(output)
        except Exception as e:
            self.respond("minidump_stackwalk failed %s" % str(e), 500)

        shutil.rmtree(session_dir)

    def dump_syms(self, form):
        # Here we will store all data including generated symbols
        session_dir = self.generateSessionDir()

        # Symbols dir
        symbols_out_dir = os.path.join(session_dir, 'symbols')
        createDirIfNotExist(symbols_out_dir)

        # .so files
        libs_dir = os.path.join(session_dir, 'libs')
        createDirIfNotExist(libs_dir)

        # Save input data
        input_file = self.save_file(session_dir, form, 'file')

        # Locate input data insise libs dir
        if input_file.endswith(".zip"):
            zip_ref = zipfile.ZipFile(input_file, 'r')
            zip_ref.extractall(libs_dir)
            zip_ref.close()
        else:
            copy2(input_file, libs_dir)

        # Run dump_syms
        for root, subdirs, files in os.walk(libs_dir):  # Recursively listdir
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
        shutil.rmtree(session_dir)  # Remove current session dir

    def generateSessionDir(self):
        SESSIONID = str(uuid.uuid4())
        print "Processing session %s" % SESSIONID
        session_dir = os.path.join(tempfile.gettempdir(), SESSIONID)
        createDirIfNotExist(session_dir)
        return session_dir

    def getHttpForm(self):
        return cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     }
        )

    def do_POST(self):
        if self.path == '/dump_syms':
            self.dump_syms(self.getHttpForm())
        elif self.path == '/minidump_stackwalk':
            self.minidump_stackwalk(self.getHttpForm())

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

    def save_file(self, session_dir, form, form_file_name):
        input_file = os.path.join(session_dir, form[form_file_name].disposition_options['filename'])
        data = form[form_file_name].file.read()
        open(input_file, "wb").write(data)
        return input_file


try:
    server = HTTPServer(('', PORT), StoreHandler)
    print 'Started httpserver on port ', PORT

    server.serve_forever()
except KeyboardInterrupt:
    print '^C received, shutting down the web server'
server.socket.close()
