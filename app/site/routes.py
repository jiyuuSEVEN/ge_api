from flask import Blueprint, request, render_template

site = Blueprint('site', __name__, template_folder='templates')

@site.route('/')
def index():
    return render_template('index.html')