'''
Website.py defines a flask blueprint that adds routes for
a mystic door website. The pages that make up the website
are taken from /templates
'''

from flask import Blueprint, render_template, request
from werkzeug import secure_filename
import os

# File upload logic

UploadFolder = 'uploads/'
AllowedExtensions = set(['xml'])

# Check file name
def allowedFilename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in AllowedExtensions

website = Blueprint("simple_page", __name__)

@website.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        submittedFile = request.files['file']
        if submittedFile and allowedFilename(submittedFile.filename):
            filename = secure_filename(submittedFile.filename)
            submittedFile.save(os.path.join(UploadFolder, filename))
            return "XML file has been received"
        else:
            return "Invalid file"
    return render_template("index.html")