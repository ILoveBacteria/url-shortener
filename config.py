import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ac%sA2S@dw!'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    @property
    def SQLALCHEMY_DATABASE_URI(cls):
        link = os.environ.get('DATABASE_URL')
        if not link.startswith('postgresql'):
            link = link.replace('postgres', 'postgresql', 1)
        return link
