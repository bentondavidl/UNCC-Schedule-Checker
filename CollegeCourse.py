from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as request

# URL to start scraping from
# starting with catalog page that needs crn concatinated
crn_page_url = "https://selfservice.uncc.edu/pls/BANPROD/bwckschd.p_disp_detail_sched?term_in=202010&crn_in="
# URL for schedule information. Needs to be formatted where {0}=prefix and {1}=course_number
schedule_url = "https://selfservice.uncc.edu/pls/BANPROD/bwckctlg.p_disp_listcrse?term_in=202010&subj_in={0}&crse_in={1}&schd_in=%25"

####################################
# I need to come back and clean up #
# data stored in attributes and    #                           
# create setters for class_time,   #
# class_days, class_location(?)    #
# *possibly separate class         #
####################################

class CollegeCourse:
    def __init__(self, crn):
        self.crn = crn
        self.course_title = ""
        self.class_name = ""
        self.class_type = ""
        self.class_method = ""
        self.class_hours = ""
        self.prefix = ""
        self.course_id = ""
        self.class_time = ""
        self.class_location = ""
        self.class_days = ""
        self.instructors = ""
        self.total_seats = ""
        self.total_enrolled = ""

        self.scrape_class_info()

    # define method to get schedule details
    def scrape_class_details(self):
        # open connection and download html
        uClient = request(schedule_url.format(self.prefix, self.course_id))

        # parse html into soup data type so it can be treated as json
        page_soup = soup(uClient.read(), 'html.parser')
        uClient.close()

        # find all sections of the course offered
        sections = page_soup.findAll('th', {'class':'ddtitle'})
        
        time, days, where, instructors = ('','','','')
        # cycle through each section and identify correct course
        for course in sections:
            if course.text == self.course_title:
                schedule_info = course.parent.findNext('table').findNext('tr').findNext('tr')
                elements = schedule_info.text.split('\n')
                time, days, where, instructors = elements[2], elements[3], elements[4], elements[7]

        return time, days, where, instructors

    def scrape_class_info(self):
        # opens the connection and downloads html from page_url
        uClient = request(crn_page_url+self.crn)

        # parses html into soup so that it can be traversed as
        # if it were a JSON data type
        page_soup = soup(uClient.read(), 'html.parser')
        uClient.close()

        # save table as starting point
        container = page_soup.find('table', {"class":"datadisplaytable"})
        self.course_title = container.tr.th.text

        # extract class prefix and course number from title
        split_title = self.course_title.split(' - ')
        self.prefix, self.course_id = split_title[2].split(' ')
        self.class_name = split_title[0]

        self.class_time, self.class_days, self.class_location, self.instructors = self.scrape_class_details()

        data_container = page_soup.find('td', {"class":"dddefault"})

        # get untagged text on the page
        lines = []
        for br in data_container.findAll('br'):
            line = br.nextSibling.strip()
            if not line is '':
                lines.append(line)

        self.class_type = lines[1]
        self.class_method = lines[2]
        self.class_credits = lines[3]

        class_size_table = data_container.table
        size_nums = class_size_table.findAll('td', {'class':'dddefault'})

        self.total_seats = size_nums[0].text
        self.total_enrolled = size_nums[1].text

    # create a simple summary of the class that can be easily read
    def summarize(self):
        print()
        print(self.class_name)
        print('--------------------------------')
        print('Delivery Method: %s' % self.class_method)
        print('Course: \t %s %s' % (self.prefix, self.course_id))
        print('This meets %s in %s on %s' % (self.class_time, self.class_location, self.class_days))
        print('Taught by: \t %s' % self.instructors)
        print('%s/%s seats are currently occupied\n' % (self.total_enrolled, self.total_seats))



