# coding=utf-8
import json
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['mooc_search']
course_col = db['courses']

class CourseInfo():
    _id = ''
    name = ''
    img_url = ''
    intro_url = ''
    platform = ''
    categories = []
    category_names = []
    school = ''
    #instructors = []
    start_time = ''
    description = ''
    about = ''
    faq = ''
    syllabus = ''

    def __init__(self, c_obj, platform):
        def expand_date(date_num):
            if date_num < 10:
                date_num = '0' + str(date_num)
            return str(date_num)
            
        if platform == 'coursera':
            #print c_obj
            course_intro_prefix = 'https://www.coursera.org/course/'
            self._id = platform + '_' + c_obj['elements'][0]['slug']
            self.name = c_obj['elements'][0]['name']
            try:
                self.img_url = c_obj['elements'][0]['photoUrl']
            except:
                self.img_url = ''
            self.intro_url = course_intro_prefix + c_obj['elements'][0]['slug']
            self.platform = platform
            self.categories = c_obj['elements'][0]['categories']
            self.category_names = [a['name'] for a in c_obj['linked']['categories.v1']]
            self.school = [p['name'] for p in c_obj['linked']['partners.v1']][0]
            try:
                self.start_time = '-'.join([expand_date(d) for d in [c_obj['linked']['v1Sessions.v1'][0]['startYear'], c_obj['linked']['v1Sessions.v1'][0]['startMonth'], c_obj['linked']['v1Sessions.v1'][0]['startDay']]])
            except:
                self.start_time = ''
            self.description = c_obj['elements'][0]['description']
            self.about = c_obj['linked']['v1Details.v1'][0]['aboutTheCourse']
            self.faq = c_obj['linked']['v1Details.v1'][0]['faq']
            self.syllabus = c_obj['linked']['v1Details.v1'][0]['courseSyllabus']
            #description =
        elif platform == 'xuetangx':
            xuetangx_intro_prefix = 'http://www.xuetangx.com'
            #print c_obj
            self._id = platform + '_' + c_obj['href'][9:-6]
            self.name = c_obj['name']
            self.img_url = c_obj['thumbnail']
            if self.img_url.startswith('/'):
                self.img_url = 'http://www.xuetangx.com' + self.img_url
            self.intro_url = xuetangx_intro_prefix + c_obj['href']
            self.platform = platform
            self.categories = c_obj['categories']
            self.category_names = c_obj['category_names']
            self.school = c_obj['org']
            try:
                self.start_time = c_obj['start_time']
            except:
                self.start_time = ''
            self.description = c_obj['subtitle']
            self.about = c_obj['about']
            try:
                self.faq = c_obj['faq']
            except:
                self.faq = ''
            try:
                self.syllabus = c_obj['syllabus']
            except:
                self.syllabus = ''
                
        elif platform == 'edx':
            edx_intro_prefix = 'http://www.edx.org'
            self._id = platform + '_' + c_obj['course_id']
            self.name = c_obj['title']
            self.img_url = c_obj['image']
            self.intro_url = edx_intro_prefix + c_obj['course_about_uri']
            self.platform = platform
            self.categories = [a['title'] for a in c_obj['subjects']]
            self.category_names = [a['title'] for a in c_obj['subjects']]
            self.school = c_obj['schools'][0]['title']
            self.start_time = c_obj['start'][0:10]
            self.description = c_obj['subtitle']
            self.about = c_obj['description']
            self.faq = c_obj['what_you_will_learn']
            self.syllabus = c_obj['syllabus']

    def save(self):
        course_col.save(self.__dict__)
