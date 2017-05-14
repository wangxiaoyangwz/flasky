# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, session, redirect, url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'#设置密匙，app.config字典存储
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')#程序使用的数据库的URL保存在配置对象SQLALCHEMY_DATABASE_URI键
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #请求结束时自动提交数据库的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)#SQLAlchemy类的实例，表示程序使用的数据库，获得flask-sqlalchemy所有功能


class Role(db.Model):
    __tablename__ = 'roles'#数据库中使用的表名
    id = db.Column(db.Integer, primary_key=True)#db.Column（1.类型类似于int，float，2.属性配置选型-主键，重复，等）
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')#user属性，'User'->Role与那个模型关联，返回与Role相关联的User对象的列表 (对象.属性.过滤器（）)

    def __repr__(self):#
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

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

