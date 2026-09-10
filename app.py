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
