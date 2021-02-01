from flask import Flask, render_template, Response, url_for, redirect, request
import io
import picamera
import servo_control as sc

app = Flask(__name__)

def initialize_camera():
    camera = picamera.PiCamera()
    camera.rotation = 180
    camera.resolution = (1280, 720)

    return camera

def get_frame(camera):
    frame = io.BytesIO()
    camera.capture(frame, format='jpeg')

    return frame.getvalue()

def send_frame():
    camera = initialize_camera()

    while True:
        frame = get_frame(camera)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_capture')
def video_capture():
    return Response(send_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move_camera_left', methods=["GET", "POST"])
def move_camera_left():
    if request.method == "POST":
        global position
        position = sc.move_servo(position, "left")
        return redirect('move_camera_left')
    else:
        return render_template('index.html')

@app.route('/move_camera_right', methods=["GET", "POST"])
def move_camera_right():
    if request.method == "POST":
        global position
        position = sc.move_servo(position, "right")
        return redirect('move_camera_right')
    else:
        return render_template('index.html')

if __name__ == "__main__":
    position = sc.initialize_servo()
    app.run(host = '0.0.0.0', debug=True)