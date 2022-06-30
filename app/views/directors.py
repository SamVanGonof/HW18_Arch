from flask_restx import Resource, Namespace, fields

from app.dao.model.director import DirectorSchema
from app.containter import director_service

director_ns = Namespace('directors', description='Views for directors')
directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

director_model = director_ns.model('Director', {
    'id': fields.Integer(required=False, description="Identifier"),
    'name': fields.String(required=True, description="Director name")
})


@director_ns.route('/')
class DirectorsViews(Resource):
    @director_ns.doc(description='Получить фильмы')
    @director_ns.response(200, 'Успешно', director_model)
    @director_ns.response(404, 'Не найден')
    def get(self):
        directors_found = director_service.get_all()

        if not directors_found:
            return f"Нет режиссеров согласно запрашиваемых параметров", 404

        return directors_schema.dump(directors_found), 200


@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    @director_ns.doc(description='Получить фильмы по id')
    @director_ns.response(200, 'Успешно', director_model)
    @director_ns.response(404, 'Не найден')
    def get(self, uid):
        director = director_service.get_one(uid)

        if not director:
            return f"Режиссер с id: {uid} не найден", 404

        else:
            return director_schema.dump(director), 200
