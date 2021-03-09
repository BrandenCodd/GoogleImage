from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Info(MethodView):
    def get(self):
        return render_template('info.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        model = gbmodel.get_model()
        model.insert(request.form['description']]
        return redirect(url_for('index'))
