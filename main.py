from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🤖 Бот работает!"

@app.route("/process", methods=["POST"])
def process():
    data = request.json

    url = data.get("url")
    filename = data.get("filename", "clip.mp4")
    start = data.get("start", "00:00:30")
    duration = data.get("duration", "00:00:30")

    try:
        os.system(f"yt-dlp -f best -o original.mp4 {url}")
        subprocess.run([
            "ffmpeg", "-ss", start, "-t", duration,
            "-i", "original.mp4", "-c", "copy", filename
        ])

        return jsonify({
            "status": "ok",
            "message": "Видео нарезано",
            "filename": filename
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
