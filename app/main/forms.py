from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(FlaskForm):#定义web表单类
    name = StringField('What is your name?', validators=[Required()])#属性，文本字段，检测函数，输入是否为空
    submit = SubmitField('Submit')#表单提交按钮
