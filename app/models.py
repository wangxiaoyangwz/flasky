# -*- coding: utf-8 -*-
from . import db,login_manager

from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
#保证数据库的安全，存储密码的散列值，核对密码时比较的是散列值，计算散列函数可复现
#生成散列值无法还原原来的密码

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property 
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)#以原始密码为输入，以字符串形式返回密码的散列值，保存在数据库中
                            #generate_password_hash(password,method=pbkdf2:sha2,salt_length=8)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)#参数数据库中取出的密码散列值，和用户输入的密码
                                               #check_password_hash(hash,password)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader#加载用户的回调函数
def load_user(user_id):
    return User.query.get(int(user_id))#参数Unicode字符串形式表示的用户标识符，返回用户对象
