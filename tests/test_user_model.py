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
    
    def test_follows(self):
    	u1=User(email='18856858578@163.com',password='cat')
    	u2=User(email='1161652587@163.com',password='cat')
    	db.session.add(u1)
    	db.session.add(u2)
    	db.session.commit()
    	self.assertFalse(u1.is_following(u2))
    	self.assertFalse(u1.is_followed_by(u2))
    	timestamp_before=datetime.utcnow()
    	u1.follow(u2)
    	db.session.add(u1)
    	db.session.commit()
    	timestamp_after=datetime.utcnow()
    	self.assertTrue(u1.is_following(u2))#u1关注了u2
        self.assertFalse(u1.is_followed_by(u2))#u1没有被u2关注
        self.assertTrue(u2.is_followed_by(u1))#
        self.assertTrue(u1.followed.count() == 1)#u1的关注数
        self.assertTrue(u2.followers.count() == 1)#关注u2的数
        f = u1.followed.all()[-1]#u1关注的人倒着排序
        self.assertTrue(f.followed == u2)#u1关注的人里有u2
        self.assertTrue(timestamp_before <= f.timestamp <= timestamp_after)#时间比较
        f = u2.followers.all()[-1]
        self.assertTrue(f.follower == u1)
        u1.unfollow(u2)#u1取消关注u2
        db.session.add(u1)
        db.session.commit()
        self.assertTrue(u1.followed.count() == 0)#u1关注人数为零
        self.assertTrue(u2.followers.count() == 0)关注u2的人数为零
        self.assertTrue(Follow.query.count() == 0)
        u2.follow(u1)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        db.session.delete(u2)
        db.session.commit()
        self.assertTrue(Follow.query.count() == 0)

    


