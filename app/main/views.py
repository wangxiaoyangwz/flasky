# -*- coding: utf-8 -*- 
#蓝本中定义程序路由
from flask import render_template, redirect, url_for, abort, flash,request,current_app, make_response
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm,EditProfileAdminForm,PostForm,NameForm,CommentForm
from .. import db
from ..models import Role, User,Permission,Post,Comment
from ..decorators import admin_required,permission_required


@main.route('/',methods=['GET','POST'])
def index():#路由，处理博客文章，分页显示博客文章
	form=PostForm()
	# form1=NameForm()
	if current_user.is_authenticated and form.validate_on_submit():
	    post=Post(body=form.body.data,author=current_user._get_current_object())#创建post实例，内容从表单中获取,作者是，P116
	                                                                            #数据库需要真正的用户对象，_get_current_object()获取真正的用户对象
	                                                                            #current_user是线程内代理对象实现，类似于用户对象，实际上是轻度包装
	    db.session.add(post)#文章传入数据库
	    return redirect(url_for('.index'))
	posts=Post.query.order_by(Post.timestamp.desc()).all()#从数据库中查询，并按照时间排序
	page=request.args.get('page',1,type=int)#c查询字符串request.args-->指出渲染的页数，没有明确指出，默认第一页，type=int 保证参数不能换成整数时，返回默认值
	show_followed=False #决定显示全部文章还是关注用户的文章
	if current_user.is_authenticated:
		show_followed=bool(request.cookies.get('show_followed',''))#cookies的show_followed字段中
	if show_followed:#如果为非空字符串
		query=current_user.followed_posts#表示显示所关注用户的文章，根据得到的值设定本地变量query的值
	else:
		query=Post.query#query的值决定获取全部文章的查询还是关注用户的文章的查询
	# pagination=Post.query.order_by(Post.timestamp.desc()).paginate(#为显示某页的记录，all()换成paginate(),参数1.【必须】页数 2、指定每页显示的记录数量
	# 	                                                           #若没有指定默认20 
	# 	                                                           #
	# 	page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], #per_page的值从程序的环境变量FLASKY_POSTS_PER_PAGE中读取
	# 	error_out=False)#3、True时请求超出范围，返回404，False时返回空列表
	pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
	posts=pagination.items
	return render_template('index.html', form=form, posts=posts,
	                       show_followed=show_followed, pagination=pagination)
@main.route('/user/<username>')#资料页面的路由
def user(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	posts=user.posts.order_by(Post.timestamp.desc()).all()#从数据库中查询，并按照时间排序
	return render_template('user.html',user=user,posts=posts)


@main.route('/edit-profile',methods=['GET','POST'])
@login_required#需要先登录
def edit_profile():
	form=EditProfileForm(user=user)
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
	return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>',methods=['GET','POST'])#用户由id指定
@login_required
@admin_required
def edit_profile_admin(id):
	user=User.query.get_or_404(id)#如果提供的id不正确，返回404错误
	form=EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email=form.email.data
		user.username=form.username.data
		user.confirmed=form.confirmed.data
		user.role=Role.query.get(form.role.data)##数字标识符表示角色选项，字段的data属性获取id查询时使用提取的id加载角色对象，
		user.name=form.name.data
		user.location=form.location.data
		user.about_me=form.about_me.data
		db.session.add(user)
		flash('The profile has been updated.')
		return redirect(url_for('.user',username=user.username))
	form.email.data=user.email
	form.username.data=user.username
	form.confirmed.data=user.confirmed
	form.role.data=user.role_id#设置字段初始值
	form.name.data=user.name
	form.location.data=user.location
	form.about_me.data=user.about_me
	return render_template('edit_profile.html',form=form,user=user)

@main.route('/post/<int:id>',methods=['GET','POST'])#id是插入数据库时分配的id，用于构建博客文章的url
def post(id):
	post=Post.query.get_or_404(id)
	form=CommentForm()#评论表单实例化
	if form.validate_on_submit():
		comment=Comment(body=form.body.data,
			            post=post,
			            author=current_user._get_current_object())
		db.session.add(comment)
		flash('Your commet has been published.')
		return redirect(url_for('.post',id=post.id,page=-1))#page=-1写在url上，所以刚提交的评论才能显示在首页
	page=request.args.get('page',1,type=int)#查询字符串中获取页数
	if page==-1:#请求评论中的最后一页
		page=(post.comments.count()-1) / \
		      current_app.config['FLASKY_COMMENTS_PER_PAGE']+1#计算评论的总和和总页数得到真正显示的页数
	pagination=post.comments.order_by(Comment.timestamp.asc()).paginate(
		page,per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
		error_out=False)
	comments=pagination.items
	return render_template('post.html',posts=[post],form=form,
		                   comments=comments,pagination=pagination)

@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
	post=Post.query.get_or_404(id)
	if current_user!=post.author and \
	        not current_user.can(Permission.ADMINISTER):#允许文章作者和管理员编辑
	    abort(403)
	form=PostForm()
	if form.validate_on_submit():
		post.body=form.body.data
		db.session.add(post)
		flash('The Post has been updated.')
		return redirect(url_for('.post',id=post.id))
	form.body.data=post.body
	return render_template('edit_post.html',form=form)

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):#关注路由和视图函数
	user=User.query.filter_by(username=username).first()
	if user is None:#当前用户没关注这个用户
		flash('Invalid user.')
		return redirect(url_for('.index'))
	if current_user.is_following(user):
		flash('You are now following %s .' % username)
		return redirect(url_for('.user',username=username))
	current_user.follow(user)#调用follow()连接两个用户
	flash('You are now following %s.'% username)
	return redirect(url_for('.user',username=username))

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))

@main.route('/followers/<username>')
def followers(username):#关注者路由和视图函数
	user=User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index'))
	page=request.args.get('page',1,type=int)
	pagination=user.followers.paginate(
		page,per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
		error_out=False)
	follows=[{'user':item.follower,'timestamp':item.timestamp}#返回的是Follow实例列表
	         for item in pagination.items]
	return render_template('followers.html',user=user,title='Followers of',endpoint='.followers',
		                    pagination=pagination,follows=follows)

@main.route('/followed-by/<username>')
def followed_by(username):#关注者路由和视图函数
	user=User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index'))
	page=request.args.get('page',1,type=int)
	pagination=user.followed.paginate(
		page,per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
		error_out=False)
	follows=[{'user':item.followed,'timestamp':item.timestamp}#返回的是Follow实例列表
	         for item in pagination.items]
	return render_template('followers.html',user=user,title='Followed by',endpoint='.followed_by',
		                    pagination=pagination,follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp

@main.route('/moderate')#管理评论的路由
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
	page=request.args.get('page',1,type=int)#得到当前页数
	pagination=Comment.query.order_by(Comment.timestamp.desc()).paginate(#
		page,per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
		error_out=False)
	comments=pagination.items#某页评论列表
	return render_template('moderate.html',comments=comments,pagination=pagination,
		                   page=page)

@main.route('/moderate/enable<int:id>')#启用路由
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):#
	comment=Comment.query.get_or_404(id)
	comment.disabled=False
	db.session.add(comment)
	return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))

@main.route('/moderate/disable/<int:id>')#禁用路由
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
	comment=Comment.query.get_or_404(id)#加载评论对象
	comment.disabled=True#设置disabled字段
	db.session.add(comment)
	return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))
                                                #查询字符串，指定页数会返回该页