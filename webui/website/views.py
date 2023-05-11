from flask import Blueprint, render_template, Response

import io
import logging
import socketserver
from http import server
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


views = Blueprint('views', __name__)
streaming = Blueprint('streaming', __name__)

@streaming.route('/stream')
def stream():
    class StreamingOutput(io.BufferedIOBase):
        def __init__(self):
            self.frame = None
            self.condition = Condition()

        def write(self, buf):
            with self.condition:
                self.frame = buf
                self.condition.notify_all()

    def generate():
        try:
            while True:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame
                yield (b'--FRAME\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            logging.warning('Removed streaming client: %s', str(e))

    output = StreamingOutput()
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
    picam2.start_recording(JpegEncoder(), FileOutput(output))

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=FRAME')


@views.route('/')
@views.route('/index.html')
def home():
    return render_template("home.html")

@views.route('/live')
def live():
    return render_template("live.html")

views.register_blueprint(streaming, url_prefix='/stream')
