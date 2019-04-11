from pymodm import CharField, IntegerField, BooleanField, DateTimeField, ObjectIdField
from pymodm.connection import connect
from pymodm import MongoModel
from app import app

connect(app.config['MONGODB_URL'])


class USER(MongoModel):
    name = CharField()
    key = CharField()
    role = IntegerField()
    mobile = CharField()
    email = CharField()
    remark = CharField()
    thumb = ObjectIdField()
    certification = ObjectIdField(blank=True)
    token = CharField()
    tenant = ObjectIdField(blank=True)
    delete = BooleanField()
    createdAt = DateTimeField()
    updatedAt = DateTimeField()
    lastLogin = DateTimeField()

    class Meta:
        collection_name = 'user'
        final = True


class CERTIFICATION(MongoModel):
    certification = CharField()
    delete = BooleanField()

    class Meta:
        collection_name = 'certification'
        final = True
