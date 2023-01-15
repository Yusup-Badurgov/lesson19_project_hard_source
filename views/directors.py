from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from decorators import auth_required, admin_required
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        new_director = request.json
        director_service.update(new_director)
        return 201, {'location': f"/directors/{new_director.id}"}

@director_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        r = director_service.get_one(did)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, did):
        director_d = request.json
        if 'id' not in director_d:
            director_d['id'] = did

        director_service.update(director_d)
        return '', 204

    @admin_required
    def delete(self, did):
        director_service.delete(did)
        return "", 204