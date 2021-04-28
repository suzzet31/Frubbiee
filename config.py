class config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = ";LcYb76AL#BI'0K&Up35D$'3ifvH4G"

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB-DB_PASSWORD = "example"

    UPLOADS ="/home/username/project/flask_test/app/static/images/uploads"

    SESSION_COOKIE_SECURE = True

    class productionConfig(Config):
        pass


class DevelopmentConfig(config):
    DEBUG = True

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB-DB_PASSWORD = "example"

    UPLOADS ="/home/username/project/flask_test/app/static/images/uploads"

    SESSION_COOKIE_SECURE = True


    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    UPLOADS = "/home/username/project/flask_test/app/static/images/uploads"