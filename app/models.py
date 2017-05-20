# -*- coding: utf-8 -*-
from . import db,login_manager

from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db

#保证数据库的安全，存储密码的散列值，核对密码时比较的是散列值，计算散列函数可复现
#生成散列值无法还原原来的密码
#关注用户 000000001 
#发表评论 000000010
#写文章   000000100    ----->permissions
#管理评论 000001000
#管理员权限 100000000

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default=db.Column(db.Boolean,default=False,index=True)#只有一个角色，角色设为默认角色
    permissions=db.Column(db.Integer)#整数位标志，各操作对应一个位位置，设为1
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():#不直接创建新角色，
        roles={
            'User':(Permission.FOLLOW|
                    Permission.COMMENT|
                    Permission.WRITE_ARTICLES,True),
            'Moderator':(Permission.FOLLOW|
                         Permission.COMMENT|
                         Permission.WRITE_ARTICLES|
                         Permission.MODERATE_COMMENTS,False),
            'Administrator':(0xff,False)
        }
        for r in roles:
            role=Role.query.filter_by(name=r).first()#通过角色名在数据库中查找角色
            if role is None:
                role=Role(name=r)
            role.permissions=roles[r][0]#修改roles数组，运行函数
            role.default=roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64))#真实姓名
    location=db.Columu(db.Sting(64))#地址
    about_me=db.Column(db.Text())#自我介绍，不需要指定最大长度
    member_since=db.Columu(db.DateTime(),default=datetime.utcnow)#注册日期，默认值是当前时间，default接受函数为默认值，在调用，
    last_seen=db.Column(db.DateTime(),default=datetime.utcmow)#最后访问日期
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed=db.Column(db.Boolean,default=False)


    def __init__(self,**kwargs):#定义默认的用户角色
        super(User,self).__init__(**kwargs)
        if self.role is None:#根据电子邮件决定设为管理员还是默认角色
            if self.email==current_app.config['FLASK_ADMIN']:
                self.role=Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role=Role.query.filter_by(default=True).first()

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

    def generate_confirmation_token(self,expiration=3600):#生成令牌，expiration指定过期时间
        s=Serializer(current_app.config['SECRET_KEY'],expiration)#类的构造函数参数是密钥
        return s.dumps({'confirm':self.id})#为指定数据生成加密签名，对数据和签名排序，生成令牌字符

    def confirm(self,token):#检验令牌
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)#解码密令，参数是
        except:
            return False
        if data.get('config')!=self.id:#检测令牌中的id和存储在current_user中一登录的用户匹配
            return False
        self.confirmed=True#若通过新添加的comfirmed属性设为True
        db.session.add(self)
        return True

    def can(self,permissions):
        return self.role is not None and \
            (self.role.permissions & permissions)==permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):#刷新用户最后访问时间，每次接到用户请求，都调用
        self.last_seen=datetime.utcnow()
        db.session.add(self)


class AnonymousUser(AnonymousUserMixin):#用户未登录时current_user的值，不许检查用户是否登陆
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user=AnonymousUser

@login_manager.user_loader#加载用户的回调函数
def load_user(user_id):
    return User.query.get(int(user_id))#参数Unicode字符串形式表示的用户标识符，返回用户对象
