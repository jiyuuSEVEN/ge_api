from flask import Blueprint, request

site = Blueprint('site', __name__)

@site.route('/')
def index():
    return '<h1>Hello world!</h1>'