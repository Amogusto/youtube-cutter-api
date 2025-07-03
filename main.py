from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import os
import subprocess

app = Flask(__name__, static_folder="static")

@app.route("/", methods=["GET"])
def home():
    return "🤖 Бот работает!"

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()

    url = data.get("url")
    filename = data.get("filename", "clip.mp4")
    start = data.get("start", "00:00:30")
    duration = data.get("duration", "00:00:30")

    original_path = "original.mp4"
    clip_path = os.path.join("static", filename)

    try:
        # Скачивание видео через yt_dlp
        ydl_opts = {
            'outtmpl': original_path,
            'format': 'best',
            'cookiefile': None,
            'cookiesfrombrowser': ('chromium',)
        }


        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Нарезка видео
        subprocess.run([
            "ffmpeg", "-ss", start, "-t", duration,
            "-i", original_path, "-c", "copy", clip_path
        ], check=True)

        # Удаление исходного видео
        if os.path.exists(original_path):
            os.remove(original_path)

        return jsonify({
            "status": "ok",
            "message": "Видео нарезано",
            "filename": filename,
            "url": f"{request.host_url}static/{filename}"
        })

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

# Раздача статичных файлов (в т.ч. нарезанных клипов)
@app.route('/static/<path:filename>')
def serve_clip(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

