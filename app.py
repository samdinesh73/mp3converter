import os
from flask import Flask, render_template, request, send_file
from moviepy import VideoFileClip
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video = request.files["video"]
        if video:
            filename = secure_filename(video.filename)
            video_path = os.path.join(UPLOAD_FOLDER, filename)
            video.save(video_path)

            mp3_filename = os.path.splitext(filename)[0] + ".mp3"
            mp3_path = os.path.join(UPLOAD_FOLDER, mp3_filename)

            clip = VideoFileClip(video_path)
            clip.audio.write_audiofile(mp3_path)

            return send_file(mp3_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
