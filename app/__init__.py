from flask import Flask
from flask_bootstrap import Bootstrap#模板
from flask_mail import Mail#邮件
from flask_moment import Moment#时间
from flask_sqlalchemy import SQLAlchemy#数据库
from config import config#导入环境配置
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail




#创建实例，创建扩展对象,没有向构造函数传入参数
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown=PageDown()

login_manager=LoginManager()
login_manager.session_protection='strong'#LoginManager对象的session_protection属性提供不同安全等级
                                         #属性可设为None、Basic、strong->记录客户端ip，浏览器的用户代理信息
login_manager.login_view='auth.login'#login_view设置登陆页面的端点，登陆路由在蓝本中定义，所以加蓝本名字


def create_app(config_name):#工厂函数，，参数是程序使用的配置名
    app=Flask(__name__)#在工厂函数中创建程序实例，延迟创建程序实例

    app.config.from_object(config[config_name])#flask app.config配置对象提供的from_object方法，使其中保存的配置导入程序
                                               #配置对象通过名字从config字典中获取
    
    #在之前创建的扩展对象调用init_app()完成初始化
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    #蓝本在工厂函数中注册到程序中
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')#url_prefix可选参数，路由会加上指定前缀
                                                             #/logic会注册为/auth/logic
    return app



