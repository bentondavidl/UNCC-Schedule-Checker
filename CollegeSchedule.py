from CollegeCourse import CollegeCourse

class CollegeSchedule:
    def __init__(self, courses):
        # verify input type
        for course in courses:
            if not isinstance(course, CollegeCourse):
                raise TypeError("courses must be an instance of CollegeCourse")
        self.courses = courses

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
    

    # TODO: Add methods for checking for overlapping courses
    # TODO: COOL STUFF!!
        
