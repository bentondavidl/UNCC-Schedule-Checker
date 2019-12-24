from flask import Flask, render_template
from ScheduleChecker.views.classes import bp as bp_classes
import ScheduleChecker.settings as settings

app = Flask(__name__)
app.register_blueprint(bp_classes)
app.config["SECRET_KEY"] = settings.API_KEY
