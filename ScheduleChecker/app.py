from ScheduleChecker import api
from flask import Flask, render_template
from ScheduleChecker.views.classes import bp as bp_classes

app = Flask(__name__)
app.register_blueprint(bp_classes)
app.config["SECRET_KEY"] = api
