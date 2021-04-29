

import os

S3_BUCKET                 = os.environ.get("S3_BUCKET_NAME")
S3_KEY                    = os.environ.get("S3_ACCESS_KEY")
S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY                = os.urandom(32)
DEBUG                     = True
PORT                      = 5000

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