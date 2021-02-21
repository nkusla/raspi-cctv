from flask import Flask, render_template, Response, url_for, redirect, request
import io
from multiprocessing import Process
import camera as c
import servo_control as sc

app = Flask(__name__)

def get_frame():
    with open("video_capture/frame.jpeg", "rb") as frame:
        frame_buf = io.BytesIO(frame.read())

    return frame_buf.getvalue()

def send_frame():
    while True:
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + get_frame() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_capture')
def video_capture():
    return Response(send_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move_camera_left', methods=["GET", "POST"])
def move_camera_left():
    if request.method == "GET":
        global position
        position = sc.move_servo(position, "left")
        return render_template('index.html')

@app.route('/move_camera_right', methods=["GET", "POST"])
def move_camera_right():
    if request.method == "GET":
        global position
        position = sc.move_servo(position, "right")
        return render_template('index.html')

if __name__ == "__main__":
    position = sc.initialize_servo()

    camera_process = Process(target=c.start_frame_capture)

    camera_process.start()
    app.run(host = '0.0.0.0', debug=True)

    camera_process.join()