 # -*- coding: utf-8 -*-
from flask import Flask,render_template
from flask_script import Manager#启动项设置，命令行解释器
from flask_bootstrap import Bootstrap#bootstrap是客户端框架，提供用户界面组件，创建网页
from flask_moment import Moment
from datetime import datetime


app = Flask(__name__)#初始化
manager = Manager(app)
bootstrap = Bootstrap(app)
moment=Moment(app)


@app.errorhandler(404)#定义错误页面
def page_not_found(e):
    return render_template('404.html'), 404
    

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():#视图函数-->生成响应
    return render_template('index.html',current_time=datetime.utcnow())#将模板集成到程序


@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)#参数传到模版中


if __name__ == '__main__':#启动服务器
    manager.run()
