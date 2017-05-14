# -*- coding: utf-8 -*-
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app=Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'#设置密匙，app.config字典存储

manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)

class NameForm(FlaskForm): #表单类
    name = StringField('What is your name?', validators=[Required()])#属性有文本字段和submit按钮
                                                                    #字段对象附属一个验证函数——>输入合法？
                                                                      #validators是一个验证函数组成的列表
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])#methods视图函数注册为GET,POST请求的处理函数
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():#检测函数
        name = form.name.data#name存放由data获取的输入名
        form.name.data = ''#清空表单字段
    return render_template('index.html', form=form, name=name)#表单实例，将其通过参数form传入模板，将data获得的输入名字传到模版中


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


if __name__=='__main__':
    manager.run()

