import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    REBLOGER_TITLE = 'Realityone\'s Blog'
    REBLOGER_DETAILS = 'A New ReBloger'
    RECENTPOST_QUANTITY = 10
    ARCHIVE_TYPE = {0: 'weekly', 1: 'monthly'}[0]
    ARCHIVE_QUANTITY = 12
    SECRET_KEY = '123456'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    REBLOGER_ADMIN = 'realityone@me.com'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'dev': DevConfig,
    'prd': ProductionConfig,
    'default': DevConfig
}
