# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'#设置密匙，app.config字典存储

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm): #表单类
    name = StringField('What is your name?', validators=[Required()])#属性有文本字段和submit按钮
                                                                    #字段对象附属一个验证函数——>输入合法？
                                                                      #validators是一个验证函数组成的列表
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])#methods视图函数注册为GET,POST请求的处理函数
def index():
    form = NameForm()
    if form.validate_on_submit():        #检测函数
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:#没有输入或输入不等于存在session中及以前输入的名字
            flash('Looks like you have changed your name!')#显示
        session['name'] = form.name.data #然后在将新输入的名字存储在用户会话中
        return redirect(url_for('index')) #刷新后，重定向URL发出GET请求，只显示网页，重新打POST请求，刷新会再次提交表单
    return render_template('index.html', form=form, name=session.get('name'))#表单实例，将其通过参数form传入模板，将data获得的输入名字传到模版中  #session.get()获取存储在用户会话名字

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


if __name__=='__main__':
    manager.run()

