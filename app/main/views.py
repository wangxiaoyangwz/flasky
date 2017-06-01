# -*- coding: utf-8 -*- 
#蓝本中定义程序路由
from flask import render_template, abort
from . import main
from ..models import User#从上上级的models中导入User



@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<username>')#资料页面的路由
def user(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	return render_template('user.html',user=user)