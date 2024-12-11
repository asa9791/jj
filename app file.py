from flask import Flask, render_template, redirect, url_for, flash
import cv2
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'supersecretkey'


def capture_image():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    if not ret:
        return None

    if not os.path.exists('captured_images'):
        os.makedirs('captured_images')

    img_path = os.path.join('captured_images', 'captured_image.jpg')
    cv2.imwrite(img_path, frame)
    camera.release()
    return img_path


def send_email(image_path):
    from_email = "your_email@example.com"
    from_password = "your_password"
    to_email = "your_email@example.com"  # ایمیل شما

    msg = MIMEMultipart()
    msg['Subject'] = 'Captured Image'
    msg['From'] = from_email
    msg['To'] = to_email

    with open(image_path, 'rb') as img_file:
        img = MIMEImage(img_file.read())
    msg.attach(img)

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/capture', methods=['GET'])
def capture():
    img_path = capture_image()
    if img_path:
        send_email(img_path)
        flash('Image captured and sent successfully!', 'success')
    else:
        flash('Error capturing image', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
