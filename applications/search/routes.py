from flask import Blueprint

search = Blueprint('search', __name__, template_folder='templates')

@search.route('/search/')
def searchRoute():
    return "Hello from search!"