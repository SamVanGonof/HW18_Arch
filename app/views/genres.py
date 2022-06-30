from flask_restx import Resource, Namespace, fields

from app.dao.model.genre import GenreSchema
from app.containter import genre_service

# Объявляем namespaces и создаем схемы
genre_ns = Namespace('genres', description='Views for genres')
genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()

# Определяем API модель
genre_model = genre_ns.model('Genre', {
    'id': fields.Integer(required=False, description="Identifier"),
    'name': fields.String(required=True, description="Genre name")
})


@genre_ns.route('/')
class GenresViews(Resource):
    @genre_ns.doc(description='Get movies')
    @genre_ns.response(200, 'Успешно', genre_model)
    @genre_ns.response(404, 'Не найден')
    def get(self):
        genres_found = genre_service.get_all()

        if not genres_found:
            return f"Нет жанров согласно запрашиваемых параметров", 404

        return genres_schema.dump(genres_found), 200


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    @genre_ns.doc(description='Получить фильм по id')
    @genre_ns.response(200, 'Успешно', genre_model)
    @genre_ns.response(404, 'Не найден')
    def get(self, uid):
        genre = genre_service.get_one(uid)

        if not genre:
            return f"Жанр с id: {uid} не найден", 404

        else:
            return genre_schema.dump(genre), 200
