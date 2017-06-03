# -*- coding: utf-8 -*- 
#蓝本中定义程序路由
from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm,EditProfileAdminForm,PostForm,NameForm
from .. import db
from ..models import Role, User,Permission,Post
from ..decorators import admin_required


@main.route('/',methods=['GET','POST'])
def index():#路由，处理博客文章，
	form=PostForm()
	# form1=NameForm()
	if form.validate_on_submit():
	    post=Post(body=form.body.data,author=current_user._get_current_object())#创建post实例，内容从表单中获取,作者是，P116
	                                                                            #数据库需要真正的用户对象，_get_current_object()获取真正的用户对象
	                                                                            #current_user是线程内代理对象实现，类似于用户对象，实际上是轻度包装，
	    db.session.add(post)#文章传入数据库
	    return redirect(url_for('.index'))
	posts=Post.query.order_by(Post.timestamp.desc()).all()#从数据库中查询，并按照时间排序
	return render_template('index.html',form=form,posts=posts)

@main.route('/user/<username>')#资料页面的路由
def user(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	posts=user.posts.order_by(Post.timestamp.desc()).all()#从数据库中查询，并按照时间排序
	return render_template('user.html',user=user)


@main.route('/edit-profile',methods=['GET','POST'])
@login_required#需要先登录
def edit_profile():
	form=EditProfileForm()
	if form.validate_on_submit():#
	    current_user.name=form.name.data#显示表单之前视图函数为字段设置初始值
	    current_user.location=form.location.data#通过form.<>.data完成
	    current_user.about_me=form.about_me.data
	    db.session.add(current_user)
	    flash('Your profile has been updated.')
	    return redirect(url_for('.user',username=current_user.username))
	form.name.data=current_user.name#当返回false时，表单中的字段使用保存在current_user中的初始值
	form.location.data=current_user.location
	form.about_me.data=current_user.about_me
	return render_template('edit_profile.html',form=form)


@main.route('/edit-profile/<int:id>',methods=['GET','POST'])#用户由id指定
@login_required
@admin_required
def edit_profile_admin(id):
	user=User.query.get_or_404(id)#如果提供的id不正确，返回404错误
	form=EditProfileAdminForm()
	if form.validate_on_submit:
		user.email=form.email.data
		user.username=form.usernmae.data
		user.confirmed=form.confirmed.data
		user.role=Role.query.get(form.role.data)##数字标识符表示角色选项，字段的data属性获取id查询时使用提取的id加载角色对象，
		user.name=form.name.data
		user.location=form.location.data
		user.about_me=form.about_me.data
		db.session.add(user)
		flash('The profile has been updated.')
		return redirect(url_for('.user',username=user.username))
	form.email.data=user.email
	form.usernmae.data=user.username
	form.confirmed.data=user.confirmed
	form.role.data=user.role_id#设置字段初始值
	form.name.data=user.name
	form.location.data=user.location
	form.about_me.data=user.about_me
	return render_template('edit_profile.html',form=form,user=user)
