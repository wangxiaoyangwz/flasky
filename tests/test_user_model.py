# -*- coding: utf-8 -*-
#
import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
	def test_password_setter(self):
		u=User(password='cat')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		u=User(password='cat')
		with self.assertRaises(AttributeError):
			u.password

	def test_password_verification(self):
		u=User(password='cat')
		self.assertTrue(u.verify_password('cat'))
		self.assertFalse(u.verify_password('dog'))

	def test_password_salts_are_random(self):
		u=User(password='cat')
		u2=User(password='cat')
		self.assertTrue(u.password_hash!=u2.password_hash)

	
	def test_roles_and_permissions(Self):
		Role.insert.roles()#数据库中创建角色
		u=User(email='18856858578@163.com',password='cat')
		self.assertTrue(u.can(Permission.WRITE_ARTICLES))
		self.assertFalse(u.can(Permission.MODERATE_COMMENTS))#断言用户没有管理评论的权限

	def test_anonymous_user(self):#匿名用户
		u=AnonymousUser()
		self.assertFalse(u.can(Permission.FOLLOW))


