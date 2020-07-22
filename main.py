import os
from collections import deque
from pathlib import Path
import socket

from flask import Flask
from flask import request, render_template, flash, send_file, redirect

UPLOAD_FOLDER = '/home/kang/file_transfer/file_received'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('202.38.64.246', 80))
app.config['IP'] = s.getsockname()[0]
s.close()
app.secret_key = 'super secret key kang'

files = deque(Path(UPLOAD_FOLDER).iterdir())
all_info = deque()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            if file:
                file.save(Path(app.config['UPLOAD_FOLDER'], file.filename))
                files.appendleft(Path(app.config['UPLOAD_FOLDER'], file.filename))
                flash(f'file {file.filename} saved!')
            else:
                flash('No file found!', 'warning')
        if 'info' in request.values:
            if request.values['info']:
                all_info.appendleft(request.values['info'])
                flash('New information received!')
    return render_template('index.html', all_info=all_info, files=files, ip=app.config['IP'])


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_file(Path(app.config['UPLOAD_FOLDER'], filename))


@app.route('/reset')
def reset():
    while files:
        os.remove(str(files.pop()))
    while all_info:
        all_info.pop()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
