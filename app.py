import os
from datetime import datetime

import qrcode
from flask import Flask, jsonify, render_template, request, send_from_directory

app = Flask(__name__)

QR_DIR = os.path.join("static", "qrcodes")
os.makedirs(QR_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html", qr_image="preview.png")  # imagem inicial


@app.route("/preview", methods=["POST"])
def preview_qr():
    data = request.json
    url = data.get("url", "") or "https://www.bravuscompany.com/"
    fill_color = data.get("fill_color", "#000000")
    bg_color = data.get("bg_color", "#ffffff")
    transparent = data.get("transparent", False)

    if transparent:
        bg_color = "transparent"  # (ou None, se depois quiser realmente transparência)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=bg_color)

    filename = f"preview.png"
    filepath = os.path.join(QR_DIR, filename)
    img.save(filepath)

    return jsonify({"qr_image": f"/static/qrcodes/{filename}"})


@app.route("/download/<filename>")
def download_qr(filename):
    return send_from_directory(QR_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
