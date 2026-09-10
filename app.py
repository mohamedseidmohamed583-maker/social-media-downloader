from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "/tmp/downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Social Media Downloader</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f2f2;
            text-align: center;
            padding: 40px 15px;
        }

        .box {
            max-width: 520px;
            margin: auto;
            background: white;
            padding: 30px 20px;
            border-radius: 18px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.10);
        }

        h1 {
            margin-bottom: 10px;
        }

        input {
            width: 90%;
            padding: 15px;
            margin: 18px 0;
            border: 1px solid #ccc;
            border-radius: 10px;
            font-size: 15px;
        }

        button {
            padding: 14px 30px;
            border: none;
            border-radius: 10px;
            background: #111;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #333;
        }

        .success {
            color: green;
            margin-top: 20px;
        }

        .error {
            color: red;
            margin-top: 20px;
        }

        .download {
            display: inline-block;
            margin-top: 15px;
            padding: 13px 25px;
            background: #16a34a;
            color: white;
            text-decoration: none;
            border-radius: 10px;
        }
    </style>
</head>

<body>

<div class="box">

    <h1>🌐 Social Media Downloader</h1>

    <p>Paste a public video URL below</p>

    <form method="POST">

        <input
            type="url"
            name="url"
            placeholder="Paste TikTok, YouTube, Instagram, Facebook URL..."
            required
        >

        <br>

        <button type="submit">
            ⬇️ Download
        </button>

    </form>

    {% if error %}
        <div class="error">
            {{ error }}
        </div>
    {% endif %}

    {% if title %}
        <div class="success">
            <b>{{ title }}</b>
            <br>

            <a class="download" href="{{ download_url }}">
                ⬇️ Download Video
            </a>
        </div>
    {% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    title = ""
    error = ""
    download_url = ""

    if request.method == "POST":

        url = request.form.get("url", "").strip()

        if not url:
            error = "❌ Please enter a URL."

        else:

            try:

                file_id = str(uuid.uuid4())

                output_template = os.path.join(
                    DOWNLOAD_FOLDER,
                    file_id + ".%(ext)s"
                )

                options = {
                    "quiet": True,
                    "noplaylist": True,
                    "outtmpl": output_template,

                    # Prefer MP4 when available
                    "format": "best[ext=mp4]/best"
                }

                with yt_dlp.YoutubeDL(options) as ydl:

                    info = ydl.extract_info(
                        url,
                        download=True
                    )

                    title = info.get(
                        "title",
                        "Video"
                    )

                    requested = ydl.prepare_filename(info)

                if os.path.exists(requested):

                    filename = os.path.basename(requested)

                    download_url = "/download/" + filename

                else:

                    # Find downloaded file if extension changed
                    files = [
                        f for f in os.listdir(DOWNLOAD_FOLDER)
                        if f.startswith(file_id)
                    ]

                    if files:

                        filename = files[0]

                        download_url = "/download/" + filename

                    else:

                        error = "❌ Downloaded file was not found."

            except Exception as e:

                print("DOWNLOAD ERROR:", e)

                error = (
                    "❌ Download failed. "
                    "Make sure the URL is public and supported."
                )

    return render_template_string(
        HTML,
        title=title,
        error=error,
        download_url=download_url
    )


@app.route("/download/<filename>")
def download_file(filename):

    file_path = os.path.join(
        DOWNLOAD_FOLDER,
        filename
    )

    if not os.path
