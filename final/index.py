from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(image=row[0], image_info=row[1] ) for row in model.select()]
        return render_template('index.html',entries=entries)

