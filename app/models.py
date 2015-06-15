# -*- coding: utf-8 -*-
from django.db import models
from django.http import HttpResponse

import json
import re

def check_cellphone(cellphone):
    if len(cellphone) > 6:
        if re.match("^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}$", phone) != None:
            return True
    return False

def check_email(email):
    if len(email) > 6:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False
    
def error(code, message):
    return {'code':code, 'message':message}
