import os
from flask import Flask, request, abort, url_for, flash, secure_filename
import whisper

wm = whisper.load_model(name="tiny", download_root="/tmp")

UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

@app.route("/")
def home():
    return "hello"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/whisper", methods=["POST"])
def handle():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        abort(400)
        return
        
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        abort(400)
        return
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return process_voice(os.path.join(app.config['UPLOAD_FOLDER'], filename))

def process_voice(filename):
    return wm.transcribe(filename)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)