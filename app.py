from flask import Flask, request, render_template_string
import yt_dlp

app = Flask(__name__)

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
            max-width: 500px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
        }
        input {
            width: 90%;
            padding: 14px;
            margin: 15px 0;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
        button {
            padding: 13px 25px;
            border: none;
            border-radius: 8px;
            background: #111;
            color: white;
            font-size: 16px;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>🌐 Social Media Downloader</h1>
        <p>Paste a supported public video URL below.</p>

        <form method="POST">
            <input
                type="url"
                name="url"
                placeholder="Paste video URL here"
                required
            >
            <br>
            <button type="submit">⬇️ Download</button>
        </form>

        {% if result %}
            <p>{{ result }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if not url:
            result = "❌ Please enter a URL."
        else:
            try:
                options = {
                    "quiet": True,
                    "noplaylist": True,
                    "skip_download": True
                }

                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=False)

                title = info.get("title", "Video")
                result = f"✅ Found: {title}"

            except Exception:
                result = (
                    "❌ This URL could not be processed. "
                    "Make sure it is a public URL and supported by the downloader."
                )

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
