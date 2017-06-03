# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField,BooleanField,SelectField
from wtforms.validators import Required,Length,Email,Regexp
from wtforms import ValidationError
from ..models import Role, User

class NameForm(FlaskForm):#定义web表单类
    name = StringField('What is your name?', validators=[Required()])#属性，文本字段，检测函数，输入是否为空
    submit = SubmitField('Submit')#表单提交按钮


class EditProfileForm(FlaskForm):#资料编辑表单
    name=StringField('Real name',validators=[Length(0,64)])#'Real name'要显示的文本框名字，validators验证函数，参数是列表，多个项，此处验证长度
    location=StringField('Location',validators=[Length(0,64)])#字段可选，可为空
    about_me=TextAreaField('About me')
    submit=SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):#管理员使用的资料编辑器
	email=StringField('Email',validators=[Required(),Length(1,64),Email()])
	username=StringField('Username',validators=[Required(),Length(1,64),
		                 Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
		                 	    'Username must have only letters,'
		                 	    'Numbers,dots or underscores')])
	confirm=BooleanField('Confirmed')
	role=SelectField('Role',coerce=int)#selectfield下拉列表，coerce=int 将字段值转换成整数，选择用户角色
	name=StringField('Real name',validators=[Length(0,64)])
	location=StringField('Location',validators=[Length(0,64)])
	about_me=TextAreaField('About me')
	submit=SubmitField('Submit')

	def __init__(self,user,*args,**kwargs):#表单的构造函数
		super(EditProfileAdminForm,self).__init__(*args,**kwargs)#继承EditProfileAdminForm的属性，使其初始化
		self.role.choices=[(role.id,role.name)#choices列表，role下拉列表，在其中设置个选项，选项是元组构成，两个元素1、标识符（id）2、显示在控件中的文本（role.name）
		                    for role in Role.query.order_by(Role.neme).all()]#使用一个查询按照字母顺序排序角色
		self.user=user

	def validate_email(self,field):#验证是否已存在在数据库中，field.data是填写资料是的字段与存储在成员变量上的字段比较，如果不同和字段已存在
		if field.data != self.user.email and \
		        User.query.filter_by(email=field.data).first():#
		    raise ValidationError('Email already registered.')

	def validate_username(self,field):
		if field.data != self.username and\
		         User.query.filter_by(username=field.data).first():
		    raise ValidationError('Usname already in use.')


