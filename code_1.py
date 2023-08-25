import os
import qrcode
from flask import Flask, render_template, request, redirect, url_for
from flask import send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['QR_FOLDER'] = './static/qr_codes'

@app.route('/')
def index():
    qr_images = []
    qr_files = os.listdir(app.config['QR_FOLDER'])
    for qr_file in qr_files:
        qr_images.append(url_for('static', filename=f'qr_codes/{qr_file}'))
    return render_template('qr.html', qr_images=qr_images)

  

@app.route('/generate_qr_code', methods=['POST'])
def generate_qr_code():
    if 'image' not in request.files:
        return redirect(request.url)

    image = request.files['image']
    fcolor=request.form['fcolor']
    bcolor=request.form['bcolor']
    if image.filename == '':
        return redirect(request.url)

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    qr_code_path = os.path.join(app.config['QR_FOLDER'], f'{os.path.splitext(image.filename)[0]}.png')

    image.save(image_path)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(image_path)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fcolor, back_color=bcolor)
    img.save(qr_code_path)

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
