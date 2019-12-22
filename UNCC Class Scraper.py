from Location import Location
from CollegeCourse import CollegeCourse
from CollegeSchedule import CollegeSchedule

# URL to start scraping from
# starting with catalog page that needs crn concatinated
crn_page_url = "https://selfservice.uncc.edu/pls/BANPROD/bwckschd.p_disp_detail_sched?term_in=202010&crn_in="
# URL for schedule information. Needs to be formatted where {0}=prefix and {1}=course_number
schedule_url = "https://selfservice.uncc.edu/pls/BANPROD/bwckctlg.p_disp_listcrse?term_in=202010&subj_in={0}&crse_in={1}&schd_in=%25"

# CRN numbers for a whole schedule
schedule = ["27350","21853","23749","20157","23191","23739","20161"]
schedule2 = ["25225", "21850", "23174", "24761", "22307", "20958"]
print()
# initialize course variables
class1 = CollegeCourse("27350")
class2 = CollegeCourse("21853")
class3 = CollegeCourse("23749")
class4 = CollegeCourse("20157")
class5 = CollegeCourse("23191")
class6 = CollegeCourse("23739")
class7 = CollegeCourse("20161")

my_schedule = CollegeSchedule([class1, class2, class3, class4, class5, class6, class7])
my_schedule.view_schedule()

print('There are no time issues with your schedule.') if len(my_schedule.find_time_issues()) == 0 else print('There may be time issues with your schedule')

try:
    bad_schedule = CollegeSchedule(schedule)
except:
    print('Type checking works')    

loc1 = class1.class_location
loc2 = class2.class_location

print(my_schedule.classes_per_day())
print(class3.summarize())
print('You are signed up for '+ str(my_schedule.course_count()) +' classes which total '+ str(my_schedule.total_hours()) +' credit hours')
# print('It takes ' + str(loc1.get_time_between(loc2)) + ' to get from '+class1.class_name+' to '+class2.class_name)
