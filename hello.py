 # -*- coding: utf-8 -*-
from flask import Flask,render_template
from flask_script import Manager#启动项设置，命令行解释器
from flask_bootstrap import Bootstrap#bootstrap是客户端框架，提供用户界面组件，创建网页


app = Flask(__name__)#初始化
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():#视图函数-->生成响应
    return render_template('index.html')#将模板集成到程序


@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)#参数传到模版中


if __name__ == '__main__':#启动服务器
    manager.run()
