# -*- coding=utf-8 -*-
#视图函数对特定权限的用户使用，自定义修饰器

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):#常规权限检查
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):#如果用户没有某权限
                abort(403)#返回错误
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
