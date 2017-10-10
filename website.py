'''
Website.py defines a flask blueprint that adds routes for
a mystic door website. The pages that make up the website
are taken from /templates
'''

from flask import Blueprint, render_template

website = Blueprint("simple_page", __name__)

@website.route("/")
def index():
    return render_template("index.html")