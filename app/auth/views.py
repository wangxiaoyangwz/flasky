# -*- coding: utf-8 -*- 
from flask import render_template
from . import auth#.代表当前目录下的所有文件

@auth.route#路由修饰器由蓝本提供
def login():
	return render_template('auth/login.html')