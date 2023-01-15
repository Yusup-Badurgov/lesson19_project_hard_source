from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from decorators import auth_required, admin_required
from implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        new_genre = request.json
        genre_service.update(new_genre)
        return 201, {'location': f"/directors/{new_genre.id}"}


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        r = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, gid):
        genre_d = request.json
        if 'id' not in genre_d:
            genre_d['id'] = gid

        genre_service.update(genre_d)
        return '', 204

    @admin_required
    def delete(self, gid):
        genre_service.delete(gid)
        return "", 204