from flask_restx import Resource, Namespace, fields
from flask import request
from marshmallow import ValidationError

from app.dao.model.movie import MovieSchema
from app.containter import movie_service

# Объявляем namespaces и создаем схемы
movie_ns = Namespace('movies', description='Views for movies')
movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

# Определяем API модель
movie_model = movie_ns.model('Movie', {
    'id': fields.Integer(required=False, description="Movie identifier"),
    'title': fields.String(required=True, description="Movie title"),
    'description': fields.String(required=True, description="Short description"),
    'trailer': fields.String(required=True, description="Link to a trailer"),
    'year': fields.Integer(required=True, description="Release year"),
    'rating': fields.Float(required=True, description="Short description"),
    'genre_id': fields.Integer(required=True, description="Genre identifier"),
    'director_id': fields.Integer(required=True, description="Director identifier")
})


@movie_ns.route('/')
class MoviesViews(Resource):
    @movie_ns.doc(description='Get movies',
                  params={'director_id': 'Director identifier',
                          'genre_id': 'Genre identifier',
                          'year': 'Release year'})
    @movie_ns.response(200, 'Success', movie_model)
    @movie_ns.response(404, 'Not found')
    def get(self):

        filters = {
            'director_id': request.args.get('director_id', type=int),
            'genre_id': request.args.get('genre_id', type=int),
            'year': request.args.get('year', type=int)
        }

        movies_found = movie_service.filter(filters)

        if not movies_found:
            return f"Нет фильмов согласно заданных параметров", 404

        return movies_schema.dump(movies_found), 200

    @movie_ns.doc(description='Добавить нового режиссера', body=movie_model)
    @movie_ns.response(201, 'Создано')
    @movie_ns.response(400, 'ValidationError')
    def post(self):
        # Получаем данные из запроса и сериализуем их
        try:
            data = movie_schema.load(request.json)

        # Выдаем неправильный запрос если переданы неверные поля
        except ValidationError as e:
            return f"{e}", 400

        else:
            movie = movie_service.create(data)
            return f"Данные добавлены с id: {movie.id}", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    @movie_ns.doc(description='Получить фильм по id')
    @movie_ns.response(200, 'Успешно', movie_model)
    @movie_ns.response(404, 'Не найден')
    def get(self, uid):
        movie = movie_service.get_one(uid)

        if not movie:
            return f"Фильм с id: {uid} не найден", 404

        else:
            return movie_schema.dump(movie), 200

    @movie_ns.doc(description='Обновить фильм по id', body=movie_model)
    @movie_ns.response(200, 'Успешно')
    @movie_ns.response(400, 'Validation error')
    @movie_ns.response(404, 'Не найден')
    def put(self, uid):
        try:
            data = movie_schema.load(request.json)
            movie = movie_service.get_one(uid)
            if not movie:
                return f"Фильм с id: {uid} не найден", 404

        except ValidationError as e:
            return f"{e}", 400

        else:
            movie_service.update(uid, data)
            return f"Фильм с id: {uid} успешно обновлен", 201

    @movie_ns.doc(description='Удалить фильм по id')
    @movie_ns.response(204, 'No content')
    @movie_ns.response(404, 'Не найден')
    def delete(self, uid):
        movie = movie_service.get_one(uid)

        if not movie:
            return f"Фильм с id: {uid} не найден", 404

        else:
            movie_service.delete(uid)
            return "", 204
