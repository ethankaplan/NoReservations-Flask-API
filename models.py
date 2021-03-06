from peewee import *
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin

DATABASE = SqliteDatabase('reservations.sqlite')

class User(UserMixin, Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()

    class Meta:
        database=DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(cls.email==email).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            raise Exception('User with that email already exists')

    @classmethod
    def verify_user(cls, email, password):
        email = email.lower()
        try:
            user = cls.select().where(cls.email==email).get()
        except cls.DoesNotExist:
            raise Exception('There is no account with this email address')
        else:
            if check_password_hash(user.password, password):
                return user
            else:
                raise Exception('Incorrect password')


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
