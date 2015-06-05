# -*- coding: utf-8 -*-
from django.db import models
from django.http import HttpResponse
from mongoengine import *

import json
import re

class Activity(Document):
    cellphone = StringFiled(required=True, max_length=100)
    name = StringField(required=True, max_length=1000)
    secure_key = StringFile(required=True, max_length=1000)
    s_form  = ListFiled(DIctField())
    reg_start = DateTimeField()
    reg_end = DateTimeField()
    description = StringField(max_length=10000)
    create_time = DateTimeField()
    update_time = DateTimeFiled()
    has_file = BooleanFiled()

class Apply(Document):
    status = StringFiled(default='wait', max_length=100)
    act_id = StringFiled(required=True, max_length=1000)
    cellphone = StringFiled(required=True, max_length=100)
    email = StringFiled(max_length=100)
    s_form = ListField(DictFiled())
    has_file = BooleanFiled()

class File(Document):
    name = StringField(max_length=100)
    display_name = StringField(max_length=100)
    description = StringField(max_length=10000)
    file_type = StringField(max_length=100)
    category = StringField(max_length=100)
    value = FileField()

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
