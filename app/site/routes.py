from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder='templates', url_prefix='/site')

@site.route('/uploader')
def index():
    return render_template('index.html', data = {'status' : 1 , 'message' : 'Success'})