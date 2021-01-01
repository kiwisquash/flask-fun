import os

# dir
base_dir = os.path.abspath(os.path.dirname(__file__))
db_prod_uri = os.path.join(base_dir, "data.sqlite")
db_dev_uri = os.path.join(base_dir, "data-dev.sqlite")


class Configuration:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.googlemail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    FLASKY_MAIL_SUBJECT_PREFIX = "[Flasky]"
    FLASKY_MAIL_SENDER = os.environ.get("FLASKY_MAIL_SENDER")
    FLASKY_ADMIN = os.environ.get("FLASKY_ADMIN")

    # not sure what this does yet...
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Configuration):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or f"sqlite:///{db_dev_uri}"


class TestConfig(Configuration):
    TESTING = True
    # in memory
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"


class ProductionConfig(Configuration):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_RUL") or f"sqlite:///{db_prod_uri}"


config = dict(
    development=DevelopmentConfig,
    testing=TestConfig,
    production=ProductionConfig,
    default=DevelopmentConfig,
)
