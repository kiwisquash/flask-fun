import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import Role, User

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def add_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def hello():
    print("hello world")


# entry point
if __name__ == "__main__":
    path = os.path.dirname(__file__)
    abs_path = os.path.abspath(path)
    app.run(debug=True)
