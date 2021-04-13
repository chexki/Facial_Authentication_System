from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from predictions import *
import cv2
import shutil

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

video_camera = None
global_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/')
# def upload_form():
#     return render_template('upload.html')

def frames():
    vidcap = cv2.VideoCapture('static/video.avi')
    count = 0
    times = 500
    while count<=10:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, times)
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join('static/captured/', "frame{:d}.jpg".format(count)), image)  # save frame as JPEG file
        count += 1
        times +=500
        print('Saving')
    return 'Done'

def refresh_paths():
    dirpath = ['static/captured/','static/uploads/']
    shutil.rmtree(dirpath[0])
    shutil.rmtree(dirpath[1])
    os.mkdir(dirpath[0])
    os.mkdir(dirpath[1])
    return 'Done'

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        refresh_paths()
        filename = secure_filename(file.filename)
        # print(type(filename))
        # print(type(load_img(filename, target_size=(300, 500))))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded')
        frames()
        first_p = liveness_predictions(filename)
        sec_p = evaluation_metric(filename,threshold=0.45)
        print(first_p,sec_p)
        return render_template('index.html', filename=filename,status= "Status : " +first_p, score= "Face " + sec_p)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True,debug=True)