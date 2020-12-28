from flask import Flask, render_template, Response,  url_for
import io
import picamera

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

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)