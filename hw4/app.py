"""
A flask app for listing charities and social services in portland.
"""
import flask
from flask.views import MethodView
from index import Index
from info import Info

app = flask.Flask(__name__)       # our Flask app

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/info/',
                 view_func=Info.as_view('info'),
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
