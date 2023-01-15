from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersViews(Resource):
    def get(self):
        rs = user_service.get_all()
        result = UserSchema(many=True).dump(rs)
        return result, 200

    def post(self):
        req_json = request.json
        new_user = user_service.create(req_json)
        return "User add", 201, {"location": f'/users/{new_user.id}'}

@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        result = UserSchema.dump(user)
        return result, 200
    def put(self, uid):
        new_user_d = request.json
        if "id" not in new_user_d:
            new_user_d["id"] = uid
        user_service.update(new_user_d)
        return "User put", 204

    def delete(self, uid):
        user_service.delete(uid)
        return "user delete", 204
