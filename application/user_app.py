from model import USER
from bson import ObjectId
from app import app
from auth import raise_status


class user_app():

    def __init__(self, requestObj=None, updateObj=None):
        self.requestObj = requestObj
        self.updateObj = updateObj
        if self.requestObj and not self.requestObj.get('delete'):
            self.requestObj['delete'] = False
        else:
            self.requestObj = {'delete': False}

    def login(self):
        try:
            user = USER.objects.get(self.requestObj)
        except USER.DoesNotExist:
            try:
                USER.objects.get({'name': self.requestObj['name']})
                return raise_status(400, '密码错误')
            except USER.DoesNotExist:
                return raise_status(400, '用户名错误')
        session = {
            'id': str(user._id),
            'name': user.name,
            'role': user.role
        }
        return session

    def user_count(self):
        try:
            count = USER.objects.raw(self.requestObj).count()
            return count
        except Exception as e:
            print('user_count error:', e)
            return raise_status(500, '后台异常')

    def user_find_all(self, page=None, pageSize=None):
        try:
            if page and pageSize:
                user = list(USER.objects.raw(self.requestObj).skip((page - 1) * pageSize).limit(pageSize))
            else:
                user = list(USER.objects.raw(self.requestObj))
        except USER.DoesNotExist:
            return []
        return user

    def get_return(self, user):
        from model import CERTIFICATION
        try:
            if user.certification is not None:
                CERTIFICATION.objects.get({'_id': user.certification._id, 'delete': False})
                certificated = True
            else:
                certificated = False
        except CERTIFICATION.DoesNotExist:
            certificated = False
        if user.tenant is None:
            tenant = None
        else:
            tenant = str(user.tenant)
        if user.thumb is None:
            thumb = None
        else:
            thumb = str(user.thumb._id)
        re = {
            "id": str(user._id),
            "name": user.name,
            "key": user.key,
            "role": user.role,
            "tenant": tenant,
            "mobile": user.mobile,
            "email": user.email,
            "remark": user.remark,
            "thumb": thumb,
            "certificated": certificated,
            "token": user.token,
            "createdAt": user.createdAt,
            "updatedAt": user.updatedAt,
            "lastLogin": user.lastLogin
        }
        return re

    def user_insert(self):
        from datetime import datetime
        try:
            user_model = USER(
                name=self.requestObj['name'],
                key=self.requestObj['key'],
                role=self.requestObj['role'],
                mobile=self.requestObj['mobile'],
                email=self.requestObj['email'],
                remark=self.requestObj['remark'],
                certification=ObjectId(self.requestObj['certification']),
                thumb=ObjectId(self.requestObj['thumb']),
                token=self.requestObj['name'] + self.requestObj['key'],
                delete=False,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            ).save()
        except Exception as e:
            print('user_insert error:', e)
            app.logger.exception(e)
            raise
        return user_model

    def user_find_one(self):
        try:
            user = USER.objects.get(self.requestObj)
            return user
        except USER.DoesNotExist:
            raise

    def user_update(self):
        from datetime import datetime
        for field in ['thumb', 'certification', 'tenant']:
            if field in self.updateObj.keys():
                self.updateObj[field] = ObjectId(self.updateObj[field])
        self.updateObj['updatedAt'] = datetime.now()
        try:
            USER.objects.raw(self.requestObj).update({'$set': self.updateObj})
        except Exception:
            raise
