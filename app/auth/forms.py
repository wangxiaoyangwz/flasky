# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required,Length,Email

class LoginForm(FlaskForm):
	email=StringField('Email',validators=[Required(),Length(1,46),Email()])#length()、Email()验证函数
	password=PasswordField('Password',validators=[Required()])
	remember_me=BooleanField('keep me logged in')#BoolleanField复选框
	submit=SubmitField('Log In')

