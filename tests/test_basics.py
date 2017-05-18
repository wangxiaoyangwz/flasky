# -*- coding: utf-8 -*- 
import unittest
from flask import current_app
from app import create_app,db

class BasicsTestCase(unittest.TestCase):
	def setUp(self):#创建测试环境
		self.app=create_app('testing')#使用测试配置创建程序
		self.app_context=self.app.app_context()#激活上下文->能在测试中使用current_app
		self.app_context.push()
		db.create_all()#创建数据库

	def tearDown(self):#删除数据库，
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_app_exists(self):#确保程序实例存在
		self.assertFalse(current_app is None)#current_app->当前激活程序的程序实例

	def test_app_is_testing(self):#确保程序在测试配置中运行
		self.assertTrue(current_app.config['TESTING'])
