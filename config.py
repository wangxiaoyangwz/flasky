
# -*- coding: utf-8 -*-
import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:#基类包含通用配置
    SECRET_KEY=os.environ.get('SECRET_KEY')or 'hard to guess string'#密钥
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True#请求结束自动提交数据库变动
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    #client.UseDefaultCredentials = true;
    MAIL_USERNAME = '18856858578@163.com'
    MAIL_PASSWORD = 'fendouingjiayou4'
    FLASKY_MAIL_SUBJECT_PREFIX='[Flasky]'#邮件主题前缀
    FLASKY_MAIL_SENDER = '18856858578@163.com'#发件人地址
    FLASKY_ADMIN = '18856858578@163.com'#从环境变量中获取收件人地址

    @staticmethod#执行对当前环境的配置的初始化，参数是程序实例
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

#子类分别定义专用配置

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config={#config字典注册了不同配置环境
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production': ProductionConfig,

    'default':DevelopmentConfig#注册默认配置，开发环境
}
