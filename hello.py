 # -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)#初始化


@app.route('/')
def index():#视图函数-->生成响应
    return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':#启动服务器
    app.run(debug=True)
