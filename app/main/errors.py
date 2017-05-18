# -*- coding: utf-8 -*- 
#蓝本中的错误处理程序
from flask import render_template
from . import main #__Init__中创建蓝本，在这里使用

#如果使用errorhandler修饰器只有蓝本中的错误才能触发处理程序
@main.app_errorhandler(404)#注册程序全局的错误处理程序  app_errorhandler
def page_not_found(e):
	return render_template('404.html'),404

@main.app_errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500

