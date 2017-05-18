# -*- coding: utf-8 -*- 
#蓝本中定义程序路由
from datetime import datetime
from flask import render_template,session,redirect,url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():#检测函数
        user = User.query.filter_by(username=form.name.data).first()#从数据库中寻找当前输入的用户名的用户
        if user is None:#该用户不存在
            user = User(username=form.name.data)#写入数据库
            db.session.add(user)#添加到用户会话
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:#
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',#发送邮件
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))#url_for()函数的一个参数是路由端点名，程序的路由中。默认是视图函数名
        #蓝本中Flask为蓝本的所有端点加上一个命名空间，在不同蓝本中使用相同的端点名，命名空间是蓝本的名字，视图函数index()注册的端点名是main.index,url_for('main.index')简写url_for('.index')
          #刷新后，重定向URL发出GET请求，只显示网页，重新打POST请求，刷新会再次提交表单
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),#表单实例，将其通过参数form传入模板，将data获得的输入名字传到模版中  
                                                             #session.get()获取存储在用户会话名字

                           current_time=datetime.utcnow())