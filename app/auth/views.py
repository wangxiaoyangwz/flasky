# -*- coding: utf-8 -*- 
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,login_required,logout_user
from . import auth#.代表当前目录下的所有文件
from ..models import User
from .forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])#路由修饰器由蓝本提供
def login():#登陆路由
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()#从数据库中加载email是当前输入
		if user is not None and user.verify_password(form.password.data):#用户存在和密码正确
			login_user(user,form.remember_me.data)#login_user()在用户会哈中将用户标记为已登录，参数1、用户，2、可选的记住我布尔值
			                                      #若为False，关闭浏览器后用户会话就会过期，若是True；浏览器中写入长期有效的cookie，可复现用户会话
			return redirect(request.args.get('next') or url_for('main.index'))#重定向目标有两种1、未授权的url，显示登陆表单
			                                                                  #原地址保存在查询字符串next参数中，从request.arg字典中读取
			                                                                  #查询字符串中没有next，重定向到首页中
		flash('Invalid username or password')#如果用户不存子或密码不正确，显示消息
	return render_template('auth/login.html',form=form)#渲染表单

@auth.route('/logout')
@login_required
def logout():
	logout_user()#删除并重设用户会话
	flash('You have been logged out.')
	return redirect(url_for('main.index'))