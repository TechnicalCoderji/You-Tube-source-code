from flask import Flask, render_template, request, send_file
from PIL import Image
import os
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist('images')

    # Open images and convert to RGB
    imgs = [Image.open(f).convert('RGB') for f in files if f]
    if not imgs:
        return "No images uploaded", 400

    # Save to PDF in memory
    pdf_bytes = BytesIO()
    imgs[0].save(pdf_bytes, save_all=True, append_images=imgs[1:], format="PDF")
    pdf_bytes.seek(0)

    return send_file(pdf_bytes, download_name='converted.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)