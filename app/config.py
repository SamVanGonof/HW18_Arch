class Config:
    DEBUG = True
    RESTX_JSON = {'ensure_ascii': False, 'indent': 2}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/movies.db'
