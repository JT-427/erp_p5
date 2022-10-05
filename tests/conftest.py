import os
import pytest

from website import create_app, db

sql = [
    "INSERT INTO employee VALUES('3776m411444236001016886422099360', '員工一', 'm', '1970-01-01', NULL, NULL, '新北市淡水區', NULL)"
]


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///' + os.path.join(os.getcwd(), 'tests/tests.db')
    })

    # other setup can go here
    db.create_all(app=app)
    with app.app_context():
        for i in sql:
            db.session.execute(i)
        db.session.commit()

    yield app

    # clean up / reset resources here
    db.drop_all(app=app)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()