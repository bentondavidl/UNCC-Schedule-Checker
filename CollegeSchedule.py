from CollegeCourse import CollegeCourse
from datetime import timedelta

class CollegeSchedule:
    def __init__(self, courses):
        # verify input type
        for course in courses:
            if not isinstance(course, CollegeCourse):
                raise TypeError("courses must be an instance of CollegeCourse")
        self.courses = courses

        self.schedule = {'M':[],'T':[],'W':[],'R':[],'F':[]}
        for course in courses:
            for day in self.schedule:
                if day in course.class_times:
                    self.schedule[day].append(course)
        for day in self.schedule:
            self.schedule[day] = sorted(self.schedule[day], key=lambda CollegeCourse: CollegeCourse.class_times[day][0])

    def course_count(self):
        return len(self.courses)

    def total_hours(self):
        total_hours = 0
        for course in self.courses:
            total_hours += float(course.class_hours.split(' ')[0])

        return total_hours

    def classes_on(self, day_letter):
        # check input type
        if not isinstance(day_letter, str) or len(day_letter) != 1:
            raise TypeError("day_letter must be a single letter")

        count = 0
        for course in self.courses:
            for day in course.class_days:
                if day == day_letter:
                    count += 1
        return count

    def classes_per_day(self):
        week_days = {'M': 0, 'T': 0, 'W': 0, 'R': 0, 'F': 0}
        for day in week_days:
            week_days[day] = self.classes_on(day)
        return week_days
    
    def view_schedule(self):
        print("\nMonday:\n--------------------------------")
        for course in self.schedule['M']:
            print(course.class_name + ": " + course.class_times['M'][0].strftime("%I:%M") +" - "+course.class_times['M'][1].strftime("%I:%M"))
        print("\nTuesday:\n--------------------------------")
        for course in self.schedule['T']:
            print(course.class_name + ": " + course.class_times['T'][0].strftime("%I:%M") +" - "+course.class_times['T'][1].strftime("%I:%M"))
        print("\nWednesday:\n--------------------------------")
        for course in self.schedule['W']:
            print(course.class_name + ": " + course.class_times['W'][0].strftime("%I:%M") +" - "+course.class_times['W'][1].strftime("%I:%M"))
        print("\nThursday:\n--------------------------------")
        for course in self.schedule['R']:
            print(course.class_name + ": " + course.class_times['R'][0].strftime("%I:%M") +" - "+course.class_times['R'][1].strftime("%I:%M"))
        print("\nFriday:\n--------------------------------")
        for course in self.schedule['F']:
            print(course.class_name + ": " + course.class_times['F'][0].strftime("%I:%M") +" - "+course.class_times['F'][1].strftime("%I:%M"))
        print()

    def find_time_issues(self):
        possible_issues = {'M':[],'T':[],'W':[],'R':[],'F':[]}
        for day in self.schedule:
            if len(self.schedule[day]) > 1:
                for i in range(0, len(self.schedule[day]) - 1):
                    current_course = self.schedule[day][i]
                    next_course = self.schedule[day][i + 1]
                    if (next_course.class_times[day][0] - current_course.class_times[day][1]) <= timedelta(minutes=25):
                        possible_issues[day].append([current_course, next_course])
        
        issues = {}
        for day in possible_issues:
            for class_change in possible_issues[day]:
                given_transition_time = class_change[1].class_times[day][0] - class_change[0].class_times[day][1]
                needed_transition_time = class_change[0].class_times[day][2].get_time_between(class_change[1].class_times[day][2])
                if given_transition_time < needed_transition_time:
                    try:
                        issues[day].append(class_change)
                    except:
                        issues[day] = class_change

        return issues


    # TODO: COOL STUFF!!
        
