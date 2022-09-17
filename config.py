import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ac%sA2S@dw!'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or os.environ.get('DATABASE_URL')
