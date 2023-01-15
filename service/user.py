import base64
import hashlib
import hmac

from flask import request
from flask_restx import abort

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        user = self.dao.get_by_username(username)
        return user

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d['password'] = self.generate_hash_password(user_d.get('password'))
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d['password'] = self.generate_hash_password(user_d.get('password'))
        self.dao.update(user_d)
        return self.dao

    def generate_hash_password(self, password):
        hashed_pass = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return base64.b64encode(hashed_pass)
    def compare_hash_password(self, hash_password, other_password):
        return hmac.compare_digest(
            base64.b64decode(hash_password),
            hashlib.pbkdf2_hmac(
                'sha256',
                other_password.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            )
        )

    def delete(self, uid):
        self.dao.delete(uid)
