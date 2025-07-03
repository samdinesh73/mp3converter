import os
from flask import Flask, render_template, request, send_file
from moviepy import VideoFileClip
from PIL import Image
from pillow_heif import register_heif_opener
from werkzeug.utils import secure_filename
import zipfile
import uuid
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
    files = request.files.getlist("video")
    if not files:
        return "No video files uploaded", 400

    session_id = str(uuid.uuid4())
    session_folder = os.path.join(UPLOAD_FOLDER, session_id)
    os.makedirs(session_folder, exist_ok=True)

    if len(files) == 1:
        file = files[0]
        filename = secure_filename(file.filename)
        input_path = os.path.join(session_folder, filename)
        file.save(input_path)

        output_filename = os.path.splitext(filename)[0] + ".mp3"
        output_path = os.path.join(session_folder, output_filename)

        clip = VideoFileClip(input_path)
        clip.audio.write_audiofile(output_path)

        return send_file(output_path, as_attachment=True)

    else:
        zip_filename = f"converted_mp3_{session_id}.zip"
        zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in files:
                filename = secure_filename(file.filename)
                input_path = os.path.join(session_folder, filename)
                file.save(input_path)

                output_filename = os.path.splitext(filename)[0] + ".mp3"
                output_path = os.path.join(session_folder, output_filename)

                clip = VideoFileClip(input_path)
                clip.audio.write_audiofile(output_path)

                zipf.write(output_path, arcname=output_filename)

        return send_file(zip_path, as_attachment=True)

@app.route("/convert_jpg", methods=["POST"])
def convert_jpg():
    files = request.files.getlist("heic_image")
    if not files:
        return "No HEIC files uploaded", 400

    session_id = str(uuid.uuid4())
    session_folder = os.path.join(UPLOAD_FOLDER, session_id)
    os.makedirs(session_folder, exist_ok=True)

    if len(files) == 1:
        # Handle single file
        file = files[0]
        filename = secure_filename(file.filename)
        heic_path = os.path.join(session_folder, filename)
        file.save(heic_path)

        jpg_filename = os.path.splitext(filename)[0] + ".jpg"
        jpg_path = os.path.join(session_folder, jpg_filename)

        image = Image.open(heic_path)
        image.save(jpg_path, "JPEG")

        return send_file(jpg_path, as_attachment=True)

    else:
        # Handle multiple files → zip result
        zip_filename = f"converted_{session_id}.zip"
        zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in files:
                filename = secure_filename(file.filename)
                input_path = os.path.join(session_folder, filename)
                file.save(input_path)

                output_filename = os.path.splitext(filename)[0] + ".jpg"
                output_path = os.path.join(session_folder, output_filename)

                image = Image.open(input_path)
                image.save(output_path, "JPEG")

                zipf.write(output_path, arcname=output_filename)

        return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
