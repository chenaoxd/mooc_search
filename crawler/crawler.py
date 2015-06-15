# coding=utf-8
import urllib2, urllib
import json
import pymongo
import threading
import time
from models import CourseInfo
from bs4 import BeautifulSoup

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['mooc_search']
course_col = db['courses']

coursera_course_list_str = open('coursera_course_list.txt').read()
xuetangx_course_list_str = open('xuetangx_course_list.txt').read()
edx_course_list_str = open('edx_course_list.txt').read()

def convert_str2course(c_str):
    print json.loads(c_str)

def coursera_course_list_url(types, start, limit):
    if len(types):
        categories_part = '&categories=' + ','.join(types)
    else:
        categories_part = ''
    return 'https://www.coursera.org/api/search.v1?fields=courseIds,suggestions,courses.v1(certificates,display,instructorIds,partnerIds,photoUrl,s12nIds,specializations,startDate,v1Details),partners.v1(homeLink,logo,name),instructors.v1(firstName,lastName,middleName,prefixName,profileId,shortName,suffixName),onDemandSpecializations.v1(courseIds,logo,partnerIds),specializations.v1(logo,partnerIds,shortName),v1Details.v1(upcomingSessionId),v1Sessions.v1(durationWeeks,hasSigTrack)&includes=courseIds,courses.v1(instructorIds,partnerIds,s12nIds,specializations,v1Details),onDemandSpecializations.v1(partnerIds),specializations.v1(partnerIds),v1Details.v1(upcomingSessionId)&extraIncludes=_facets&q=search&languages=en,zh,zh-cn%s&start=%s&limit=%s&courseType=v1.session,v2.ondemand&cdpViews=HIUPOchIEeSA1yIACye2oA,v1-11,v1-225,v1-2401,v1-29,v1-77&userLanguage=en-us' % (categories_part, start, limit)

def coursera_course_detail_url(course_slug):
    return 'https://www.coursera.org/api/courses.v1?fields=categories,certificates,description,display,instructorIds,membershipIds,partnerIds,partnerLogo,photoUrl,previewLink,primaryLanguages,specializations,subtitleLanguages,v1Details,workload,memberships.v1(vcMembershipId),partners.v1(classLogo,homeLink,links,logo,name,shortName),v1Details.v1(aboutTheCourse,courseFormat,courseSyllabus,faq,ondemandCourseSlug,readings,recommendedBackground,sessionIds,upcomingSessionId,videos),v1Sessions.v1(active,dbEndDate,durationString,hasSigTrack,instructorIds,selfStudy,startDay,startMonth,startYear,status,vcDetails),instructors.v1(firstName,fullName,lastName,middleName,partnerIds,partners,photo,prefixName,profileId,shortName,suffixName),v1VcDetails.v1(vcPrice,vcRegistrationOpen,vcRegularPrice),languages.v1(englishName),specializations.v1(logo,name,partnerIds,shortName)&includes=categories,instructorIds,membershipIds,partnerIds,primaryLanguages,specializations,subtitleLanguages,v1Details,memberships.v1(vcMembershipId),v1Details.v1(sessionIds),v1Sessions.v1(instructorIds,vcDetails),instructors.v1(partnerIds),specializations.v1(partnerIds)&q=slug&slug=%s&courseType=v1.session' % course_slug

def xuetangx_course_list_url():
    return 'http://www.xuetangx.com/courses/search?cid=0&offset=0&limit=500&query=&started=false&hasTA=false&org='

def edx_course_list_url():
    return 'https://www.edx.org/search/api/all'

def ne_course_list_url():
    return ''

def get_method(url):
    conn = urllib2.urlopen(url)
    content = conn.read()
    return content

def dump_coursera_course_list():
    course_list = []
    with open('coursera_course_list.txt', 'w') as coursera_course_list_file:
        for start in [0, 200, 400, 600, 800]:
            course_list += json.loads(get_method(coursera_course_list_url([], start, 200)))['linked']['courses.v1']
        coursera_course_list_file.write(json.dumps(course_list))

def dump_xuetangx_course_list():
    course_list = []
    with open('xuetangx_course_list.txt', 'w') as xuetangx_course_list_file:
        #print get_method(xuetangx_course_list_url())
        course_list += json.loads(get_method(xuetangx_course_list_url()))['data']
        xuetangx_course_list_file.write(json.dumps(course_list))

def dump_edx_course_list():
    course_list = []
    with open('edx_course_list.txt', 'w') as edx_course_list_file:
        edx_course_list_file.write(get_method(edx_course_list_url()))

def process_edx_course_page(course_page, course_info):
    course_info_api = 'https://www.edx.org/api/catalog/v2/courses/'
    
    soup = BeautifulSoup(course_page)
    data_course_id = soup.select('main#course-info-page')[0]['data-course-id']

    course_info = json.loads(get_method(course_info_api + data_course_id))
    return course_info

def get_edx_course_detail(course_info):
    edx_course_url = ''
    
    course_page = get_method(edx_course_url + course_info['url'])

    course_info = process_edx_course_page(course_page, course_info)

    return course_info

def process_xuetangx_course_page(course_page, course_info):
    soup = BeautifulSoup(course_page)
    course_detail = [str(a) for a in soup.select('div.left.fl')[2].select('section')]

    course_info['about'] = course_detail[0]
    try:
        course_info['syllabus'] = course_detail[1]
    except:
        ''
    try:
        course_info['faq'] = course_detail[2]
    except:
        ''

    try:
        course_info['start_time'] = soup.select('section.wrap.apply.apply_loading')[0]['data-enrollment_start']
    except:
        ''

    course_info['categories'] = list(set([a.string.split('(')[0] for a in soup.select('div.right.fl section.kcxx p.about a')]))
    course_info['category_names'] = course_info['categories']
    #print course_info['categories']

    return course_info
        
def get_xuetangx_course_detail(course_info):
    xuetangx_course_url = 'http://xuetangx.com'
    course_page = get_method(xuetangx_course_url + course_info['href'])

    course_info = process_xuetangx_course_page(course_page, course_info)
        
    return course_info

def dump_edx_course(course):
    course_info = get_edx_course_detail(course)
    ci = CourseInfo(course_info, 'edx')
    ci.save()

def dump_coursera_course(course):
    try:
        course_info = json.loads(get_method(coursera_course_detail_url(urllib.quote_plus(course['slug']))))
    except:
        print course['slug'], 'insert failed...'
        return 

    ci = CourseInfo(course_info, 'coursera')
    ci.save()
    print course['slug'], 'inserted...'

def dump_xuetangx_course(course):
    course_info = get_xuetangx_course_detail(course)
    ci = CourseInfo(course_info, 'xuetangx')
    ci.save()

if __name__ == '__main__':
    print __file__, 'running...'
    #print get_method(coursera_course_list_url([]))
    #convert_str2course(course_str)
    #ci = CourseInfo(json.loads(course_str), 'coursera')
    #ci.save()

    counter = 0
    for course in json.loads(coursera_course_list_str):
        while threading.active_count() >= 100:
            print 'sleeping'
            time.sleep(3)
        t = threading.Thread(target=dump_coursera_course, args=(course,))
        t.start()
        
        if counter % 20 == 0:
            print counter
        counter += 1
            

if __name__ == '__main__':
    print __file__, 'running...'
    counter = 0
    for course in json.loads(xuetangx_course_list_str):
        while threading.active_count() >= 100:
            print 'sleeping'
            time.sleep(3)
        t = threading.Thread(target=dump_xuetangx_course, args=(course,))
        t.start()
        
        if counter % 20 == 0:
            print counter
        counter += 1

if __name__ == '__main__2':
    with open('tmp.txt') as tmp_file:
        course_page = tmp_file.read()
    for a in process_xuetangx_course_page(course_page):
        print a

if __name__ == '__main__2':
    dump_edx_course_list()

if __name__ == '__main__':
    counter = 0
    for course in json.loads(edx_course_list_str):
        while threading.active_count() >= 100:
            print 'sleeping'
            time.sleep(3)
        t = threading.Thread(target=dump_edx_course, args=(course,))
        t.start()

        if counter % 30 == 0:
            print counter
        counter += 1
    
