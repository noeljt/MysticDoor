'''
Website.py defines a flask blueprint that adds routes for
a mystic door website. The pages that make up the website
are taken from /templates
'''

from flask import Blueprint, render_template, request

website = Blueprint("simple_page", __name__)

@website.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        return "Adventure XML has been received"
    return render_template("index.html")