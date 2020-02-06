# imports
import os
# Flask
from flask import Flask, render_template, jsonify, request, Response, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
# Sessions
from uuid import uuid4
# Time
import time
# CSV
import csv
# Analyse 
from analysis import analyse

# APP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is my secret key!'
# Bootstrap
Bootstrap(app)

# Static path
static_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"))
# Uploads path
uploads_path = os.path.join(static_path, "uploads")
app.config['UPLOAD_FOLDER'] = uploads_path
# Pattern for folder names
PATTERN = 'Air-Quality'


# LANDING
@app.route('/')
def index():
	
    return render_template('index.html')


# UPLOAD FILES
@app.route('/upload', methods=['GET', 'POST'])
@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():

    # POST files
    if request.method == 'POST' and 'captures' in request.files:
        # Files
        files = request.files.getlist('captures')
        if len(files) == 0 or (len(files) == 1 and files[0].filename.strip() == ''):
            flash('No files selected')
        else:
            print('Number of files to upload: {}'.format(len(files)))
            # Create a unique "session ID" for this particular batch of uploads
            upload_key = str(uuid4())
            # Pattern for file names
            dir_name = PATTERN + '-' + time.strftime("%Y%m%d-%H%M%S") + '-' + upload_key
            directory = os.path.join(app.config['UPLOAD_FOLDER'], dir_name)
            # Create dir
            os.mkdir(directory)
            # Save files
            for i, f in enumerate(files):
                # Name
                name = f.filename
                # Save file
                filename = os.path.join(directory, name)
                f.save(filename)
            # Run analysis
            values = run_analysis(directory)
            # See Gallery
            return redirect(url_for('gallery'))

    # GET
    return render_template('upload.html')


# Analysis
def run_analysis(directory):

    # Run the analysis
    print('Starting the analysis...')
    values = analyse(directory)

    return values


# GALLERY
@app.route('/gallery')
@app.route('/gallery/')
def gallery():

    images = []

    # Get images in the uploads dir
    for name in [ filename for filename in os.listdir(app.config['UPLOAD_FOLDER']) if filename.startswith(PATTERN) ]:
        # Image path
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        image_name = [ filename for filename in os.listdir(path) if filename.endswith('.jpg') ][0] # grab the first image
        image_path = os.path.join('uploads', name, image_name)
        # Desc
        desc = '-'.join(name.split('-')[2:4]).title()
        # Add
        images.append( dict(name=name, desc=desc, image_path=image_path) )

    return render_template('gallery.html', images=sorted(images, key=lambda k: k['name']))


# VIEW
@app.route('/gallery/<name>')
@app.route('/gallery/<name>/')
def show_figure(name):

    # Get values
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], name, 'normalized', 'values.csv')
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        values = [ row for row in reader ]
    # Desc
    desc = '-'.join(name.split('-')[2:4]).title()

    return render_template('view.html', desc=desc, values=values)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)