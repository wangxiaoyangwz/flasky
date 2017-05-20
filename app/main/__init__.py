# -*- coding: utf-8 -*- 
#单脚本程序，程序实例存在全局作用域，路由可app.route直接定义
#在运行时创建程序，调用create_app后才能使用app.route

#蓝本可定义路由，且处于休眠状态。注册到程序中，才成为程序的一部分
#app/main/__init__.py中创建蓝本

from flask import Blueprint

main=Blueprint('main',__name__)#实例化Bluepirnt类对象，参数1、蓝本名字 2、蓝本所在包和模块，大多数使用python的__name__变量

from . import views,errors#导入这两个模块将程序与蓝本联系起来，在脚本末尾导入，避免循环导入，在这两个模版中要导入蓝本main
