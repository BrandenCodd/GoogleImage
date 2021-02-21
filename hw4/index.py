from flask import render_template
from flask.views import MethodView
import gbmodel

class Index(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(name=row[0], description=row[1], streetAddress=row[2], typesOfService=row[3], phoneNumber=row[4], hoursOfOperation=row[5], reviews=row[6] ) for row in model.select()]
        return render_template('index.html',entries=entries)
