from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

# Folder to save downloaded videos
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the YouTube video URL from the form
        url = request.form.get("url")
        if not url:
            return render_template("index.html", error="Please enter a valid YouTube URL.")

        try:
            # Create a YouTube object
            yt = YouTube(url)

            # Check if it's a playlist
            if "list=" in url:
                return render_template("index.html", error="Playlists are not supported.")

            # Get the best stream with 1080p preference
            stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution="1080p").first()
            if not stream:
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            if not stream:
                return render_template("index.html", error="No suitable stream found.")

            # Download the video
            output_path = stream.download(output_path=DOWNLOAD_FOLDER)
            filename = os.path.basename(output_path)

            # Provide the download link
            return render_template("index.html", title=yt.title, filename=filename)

        except Exception as e:
            return render_template("index.html", error=f"An error occurred: {e}")

    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    # Serve the downloaded file
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
