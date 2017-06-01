# -*- coding: utf-8 -*- 
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth#.代表当前目录下的所有文件
from ..models import User
from .forms import LoginForm
from .. import db
from ..email import send_email
from .forms import LoginForm, RegistrationForm


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


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required#需要先登录才能显示confirm视图函数
def confirm(token):#令牌在user模型中创建，此处只需调用confirm()
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):#confirm方法返回true，
        flash('Your have confirmed your account.Thinks!')#已证明
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.before_app_request#决定用户确认前可以做什么操作
def before_request():#允许未确认的用户登陆
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5]!='auth.' \
            and request.endpoint!='static':
        return redirect(url_for('auth.unconfirmed'))#但是显示未登录的页面

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token=current_user.generate_confirmation_token()#生成令牌
    send_email(user.email,"Confirm Your Account",
               'auth/email/confirm',user=user,token=token)#发送邮件
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))