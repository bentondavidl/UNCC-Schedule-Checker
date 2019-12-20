from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as request

# URL to start scraping from
# starting with catalog page that needs crn concatinated
crn_page_url = "https://selfservice.uncc.edu/pls/BANPROD/bwckschd.p_disp_detail_sched?term_in=202010&crn_in="
# URL for schedule information. Needs to be formatted where {0}=prefix and {1}=course_number
schedule_url = "https://selfservice.uncc.edu/pls/BANPROD/bwckctlg.p_disp_listcrse?term_in=202010&subj_in={0}&crse_in={1}&schd_in=%25"

# CRN numbers for a whole schedule
schedule = ["27350","21853","23749","20157","23191","23739","20161"]

# define method to get schedule details
def get_schedule_details(prefix, course_number, course_title):
    # open connection and download html
    uClient = request(schedule_url.format(prefix, course_number))

    # parse html into soup data type so it can be treated as json
    page_soup = soup(uClient.read(), 'html.parser')
    uClient.close()

    # find all sections of the course offered
    sections = page_soup.findAll('th', {'class':'ddtitle'})
    
    # cycle through each section and identify correct course
    for course in sections:
        if course.text == course_title:
            schedule_info = course.parent.findNext('table').findNext('tr').findNext('tr')
            elements = schedule_info.text.split('\n')
            time, days, where, instructors = elements[2], elements[3], elements[4], elements[7]

    return time, days, where, instructors


# items to track
classes = []
total_credits = 0.00

# loop through each CRN number to get class information
for crn in schedule:
    # opens the connection and downloads html from page_url
    uClient = request(crn_page_url+crn)

    # parses html into soup so that it can be traversed as
    # if it were a JSON data type
    page_soup = soup(uClient.read(), 'html.parser')
    uClient.close()

    # save table as starting point
    container = page_soup.find('table', {"class":"datadisplaytable"})
    course_title = container.tr.th.text

    # extract class prefix and course number from title
    split_title = course_title.split(' - ')
    prefix, course_number = split_title[2].split(' ')
    class_title = split_title[0]

    time, days, where, instructors = get_schedule_details(prefix, course_number, course_title)

    data_container = page_soup.find('td', {"class":"dddefault"})

    # get untagged text on the page
    lines = []
    for br in data_container.findAll('br'):
        line = br.nextSibling.strip()
        if not line is '':
            lines.append(line)

    class_type = lines[1]
    class_method = lines[2]
    class_credits = lines[3]

    class_size_table = data_container.table
    size_nums = class_size_table.findAll('td', {'class':'dddefault'})

    seats = size_nums[0].text
    enrolled = size_nums[1].text

    classes.append(class_title)
    total_credits = total_credits + float(class_credits.split(' ')[0])

    print(class_title)
    print(class_type)
    print(class_method)
    print(class_credits)
    print(enrolled + '/' + seats)
    print(days)
    print()

print('You are signed up for '+ str(len(classes))+' classes which total '+str(total_credits) +' credit hours')
