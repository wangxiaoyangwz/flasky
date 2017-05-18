# -*- coding: utf-8 -*- 
#__init__.py中创建蓝本
from flask import Blueprint

auth=Blueprint('auth',__name__)

from . import views
