import os
from flask import Flask, render_template, request, send_file
from moviepy import VideoFileClip
from PIL import Image
from pillow_heif import register_heif_opener
from werkzeug.utils import secure_filename

# Register HEIC support
register_heif_opener()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert_mp3", methods=["POST"])
def convert_mp3():
    if "video" in request.files:
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
    return "No video file uploaded", 400

@app.route("/convert_jpg", methods=["POST"])
def convert_jpg():
    if "heic_image" in request.files:
        heic_file = request.files["heic_image"]
        if heic_file:
            filename = secure_filename(heic_file.filename)
            heic_path = os.path.join(UPLOAD_FOLDER, filename)
            heic_file.save(heic_path)

            jpg_filename = os.path.splitext(filename)[0] + ".jpg"
            jpg_path = os.path.join(UPLOAD_FOLDER, jpg_filename)

            image = Image.open(heic_path)
            image.save(jpg_path, "JPEG")

            return send_file(jpg_path, as_attachment=True)
    return "No HEIC file uploaded", 400

if __name__ == "__main__":
    app.run(debug=True)
