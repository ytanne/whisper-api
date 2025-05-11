from flask import Flask
from flask import request
import whisper

wm = whisper.load_model(name="tiny", download_root="/tmp")

app = Flask(__name__)

tmp_folder = '/tmp'


@app.route("/")
def home():
    return "hello"


@app.route("/whisper", methods=["POST"])
def handle():
    filename = request.form['filename']
    response = process_voice(tmp_folder + '/' + filename)
    return response


def process_voice(filename):
    return wm.transcribe(filename)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)