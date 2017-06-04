 # -*- coding: utf-8 -*- 
#启动脚本
import os
from app import create_app, db
from app.models import User, Role, Permission,Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')#先创建程序实例，在__init__.py中定义，
                                                      #参数从环境变量FLASK_CONFIG中读取配置名or默认值
manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission,
                Post=Post) #右边app是指hello.py中的实例对象，左边app是自己命名，
	                                               #以后可以在命令行中输入，就调用了app实例

manager.add_command("shell",Shell(make_context=make_shell_context))#make_context参数是规定要传入的上下文环境

manager.add_command("db",MigrateCommand)

@manager.command
def test():
	"""Run the unit test."""
	import unittest
	tests=unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
	manager.run()