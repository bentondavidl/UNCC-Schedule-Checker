from flask import Blueprint, render_template, request, redirect, session
from ScheduleChecker.CollegeSchedule import CollegeSchedule
from ScheduleChecker.CollegeCourse import CollegeCourse
import jsonpickle

bp = Blueprint(
    __name__.split('.')[-1],
    __name__.split('.')[-1], 
    template_folder='templates'
)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        crns = request.form.get('crns').replace(' ','').split(',')
        
        courses = []
        for crn in crns:
            courses.append(CollegeCourse(crn))
        
        schedule = CollegeSchedule(courses)
        schedule.export_schedule()

        return redirect('/courses')

    return render_template('enter_classes.html')

@bp.route('/courses')
def view_courses():
    with open('schedules.json', 'r') as f:
        schedule = jsonpickle.decode(f.read())

    classes = {'M':[],'T':[],'W':[],'R':[],'F':[]}
    for day in schedule.schedule:
        classes[day] = schedule.schedule[day]

    issues = schedule.find_time_issues()
    return render_template('review_schedule.html', classes=classes, issues=issues)