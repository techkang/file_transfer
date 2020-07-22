import os
from collections import deque, defaultdict
from pathlib import Path

from flask import Flask
from flask import request, render_template, flash, send_file, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/kang/file_transfer/file_received'
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key kang'

files = defaultdict(deque)
all_info = defaultdict(deque)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'username' in request.values:
            username = request.values['username']
            if username and username == secure_filename(username):
                return redirect(username)
    return render_template('index.html')


@app.route('/<username>', methods=['POST', 'GET'])
def file_transfer(username):
    print('enter main page')
    username = secure_filename(username)
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            if file:
                folder = Path(app.config['UPLOAD_FOLDER'], username)
                folder.mkdir(exist_ok=True)
                file.save(folder / file.filename)
                files[username].appendleft(folder / file.filename)
                flash(f'file {file.filename} saved!')
            else:
                flash('No file found!', 'warning')
        if 'info' in request.values:
            if request.values['info']:
                all_info[username].appendleft(request.values['info'])
                flash('New information received!')
    return render_template('file_transfer.html', all_info=all_info[username], files=files[username], username=username)


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_file(Path(app.config['UPLOAD_FOLDER'], filename))


@app.route('/reset/<username>')
def reset(username):
    username = secure_filename(username)
    folder = Path(app.config['UPLOAD_FOLDER'], username)
    if folder.is_dir():
        for file in folder.iterdir():
            os.remove(str(file))
        folder.rmdir()
    if username in files:
        files.pop(username)
    if username in all_info:
        all_info.pop(username)
    print('finish cleaning', username)
    return redirect(url_for('file_transfer', username=username))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
