import pywhatkit as kit
from flask import Flask
from flask import request, render_template, redirect, jsonify, send_from_directory, current_app, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/upload/'

app.secret_key = 'godisbitch'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def convert_ti_text(text):
    kit.text_to_handwriting(text, "static/upload/text.png", [0,0,128])

@app.route('/home')
def hello_world():
    return render_template('index.html')
@app.route('/')
def home():
    return redirect('/home')

@app.route('/', methods=['GET', 'POST'])
def get_text():
    if request.method == 'POST':
        try:
            filename = 'text.png'
            text = request.form['input_text']
            convert_ti_text(text)
            location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return render_template('index.html', filename=filename)
        except:
            return "error"
    else:
        return redirect(request.url)
    # text = request.form.get('text')
    # convert_ti_text(text)
@app.route('/display/<filename>')
def display(filename):
    return redirect(url_for('static', filename='upload/' + filename), code=301)

@app.route('/download_image/<filename>', methods=['GET','POST'])
def download_image(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=filename)

if __name__ == '__main__':
    app.run(debug=True)