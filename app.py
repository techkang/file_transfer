import os
from collections import deque, defaultdict
from pathlib import Path

from flask import Flask, request, render_template, flash, send_file, redirect, url_for, current_app
from werkzeug.utils import secure_filename

# alert: change to your username here after 'home'
app = Flask(__name__)
app.secret_key = 'super secret key kang'

files = defaultdict(deque)
all_info = defaultdict(deque)


def init():
    upload_folder = Path(current_app.root_path, 'file_received')
    Path(upload_folder).mkdir(parents=True, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder


@app.route('/', methods=['POST', 'GET'])
def index():
    if not app.config.get('UPLOAD_FOLDER'):
        init()
    if request.method == 'POST':
        if 'username' in request.values:
            username = request.values['username']
            if username and username == secure_filename(username):
                return redirect(username)
    return render_template('index.html')


@app.route('/<username>', methods=['POST', 'GET'])
def file_transfer(username):
    if not app.config.get('UPLOAD_FOLDER'):
        init()
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


@app.route('/download/<username>/<filename>', methods=['GET', 'POST'])
def download(username, filename):
    return send_file(Path('file_received', username, filename))


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
