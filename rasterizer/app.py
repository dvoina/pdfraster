import os
from subprocess import check_call
from uuid import uuid1

from flask import Flask, flash, redirect, request, send_file, url_for, abort
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/image/<image>', methods=['GET', 'DELETE'])
def display(image):
    if request.method == 'DELETE':
        path = os.path.join(UPLOAD_FOLDER, image)
        os.removedirs(path)
        return "", 200
    send_file(os.path.join(UPLOAD_FOLDER, image, image+"-0.png"))
    

@app.route('/raster', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('upload_file', filename=filename))
            if filename.split(".")[-1]=="pdf":
                u = str(uuid1())
                path = os.path.join(UPLOAD_FOLDER, u)
                os.mkdir(path)
                dest = os.path.join(path, u+".png")
                if check_call(["convert", "-density", "72", filename, dest]) == 0:
                    if os.path.exists(dest):
                        return send_file(dest, mimetype="image/png")
                    else:
                        dest = dest.replace(".png", "-0.png")
                        return send_file(dest, mimetype="image/png")
                return abort(404)
            else:
                return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), mimetype='image/*')
                
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.debug = False
    app.run(host="0.0.0.0", port=80)
