import os
import tempfile
import pytest
import json
import main

db = main.model.db


@pytest.fixture
def client():
    db_fd, path = tempfile.mkstemp()
    main.app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{path}"
    main.app.config["TESTING"] = True
    with main.app.test_client() as client:
        with main.app.app_context():
            db.init_app(main.app)
            db.create_all()
            yield client

    os.close(db_fd)
    os.unlink(path)


def test_years_empty(client):
    """ Empty case  """
    rv = client.get("/api/years")
    data = json.loads(rv.data)
    assert len(data) == 0


def test_years_with_1_item(client):
    """ 1 Projects 1 years  """
    new_project = main.model.Project(
        uuid="G110B02",
        name="meow",
        year=110,
    )
    db.session.add(new_project)
    db.session.commit()
    rv = client.get("/api/years")
    db.drop_all()
    db.create_all()
    data = json.loads(rv.data)
    assert 110 in data


def test_years_with_multi_item(client):
    """ 2 Projects 2 years  """
    db.session.add(
        main.model.Project(
            uuid="G108B01",
            name="meow",
            year=108,
        )
    )
    db.session.add(
        main.model.Project(
            uuid="G109B02",
            name="meow",
            year=109,
        )
    )

    db.session.commit()
    rv = client.get("/api/years")
    db.drop_all()
    db.create_all()
    data = json.loads(rv.data)
    assert len(data) == 2
    assert 109 in data
    assert 108 in data


def test_login_success_student(client):
    """ Login with correct studnet account  """
    username = "meow123"
    password = "123@C@t"
    db.session.add(main.model.Student(
        username=username,
        password=password,
    ))
    db.session.commit()
    rv = client.post("/api/auth", data=json.dumps(dict(
        username=username,
        password=password
    )), content_type='application/json')
    assert rv.status_code == 200


def test_login_success_teacher(client):
    """ Login with correct teacher account  """
    username = "meow123"
    password = "123@C@t"
    db.session.add(main.model.Teacher(
        username=username,
        password=password,
    ))
    db.session.commit()
    rv = client.post("/api/auth", data=json.dumps(dict(
        username=username,
        password=password
    )), content_type='application/json')
    assert rv.status_code == 200


def test_login_success_admin(client):
    """ Login with correct admin account  """
    username = "meow123"
    password = "123@C@t"
    db.session.add(main.model.Admin(
        username=username,
        password=password,
    ))
    db.session.commit()
    rv = client.post("/api/auth", data=json.dumps(dict(
        username=username,
        password=password
    )), content_type='application/json')
    assert rv.status_code == 200


def test_login_failed_student(client):
    """ Login with incorrect studnet account  """
    username = "meow123"
    password = "123@C@t"
    noise = "@$%^&*('')"
    db.session.add(main.model.Student(
        username=username,
        password=password,
    ))
    db.session.commit()
    rv = client.post("/api/auth", data=json.dumps(dict(
        username=username,
        password=password+noise
    )), content_type='application/json')
    assert rv.status_code == 400


def test_login_failed_teacher(client):
    """ Login with incorrect teacher account  """
    username = "meow123"
    password = "123@C@t"
    noise = "@$%^&*('')"
    db.session.add(main.model.Teacher(
        username=username,
        password=password,
    ))
    db.session.commit()
    rv = client.post("/api/auth", data=json.dumps(dict(
        username=username,
        password=password+noise
    )), content_type='application/json')
    assert rv.status_code == 400


def test_login_failed_admin(client):
    """ Login with incorrect admin account  """
    username = "meow123"
    password = "123@C@t"
    noise = "@$%^&*('')"
    db.session.add(main.model.Admin(
        username=username,
        password=password,
    ))
    db.session.commit()
    rv = client.post("/api/auth", data=json.dumps(dict(
        username=username,
        password=password+noise
    )), content_type='application/json')
    assert rv.status_code == 400


def test_change_password_student(client):
    """ Change password with correct student token and password  """
    user_model = main.model.Student
    username = "meow123"
    password = "123@C@t"
    new_password = "C@t__me0w"
    db.session.add(user_model(
        username=username,
        password=password,
    ))
    db.session.commit()
    rv = client.post("/api/auth", data=json.dumps(dict(
        username=username,
        password=password
    )), content_type='application/json')
    jwt = json.loads(rv.data)
    rv = client.post("/api/change_password", data=json.dumps({
        "original_pass": password,
        "pass": new_password
    }), content_type='application/json', headers={'Authorization': jwt})
    assert user_model.query.filter_by(
        username=username).first().password == new_password
    assert rv.status_code == 200


def test_change_password_teacher(client):
    """ Change password with correct teacher token and password  """
    user_model = main.model.Teacher
    username = "meow123"
    password = "123@C@t"
    new_password = "C@t__me0w"
    db.session.add(user_model(
        username=username,
        password=password,
    ))
    db.session.commit()
    rv = client.post("/api/auth", data=json.dumps(dict(
        username=username,
        password=password
    )), content_type='application/json')
    jwt = json.loads(rv.data)
    rv = client.post("/api/change_password", data=json.dumps({
        "original_pass": password,
        "pass": new_password
    }), content_type='application/json', headers={'Authorization': jwt})
    assert user_model.query.filter_by(
        username=username).first().password == new_password
    assert rv.status_code == 200


def test_change_password_admin(client):
    """ Change password with correct admin token and password  """
    user_model = main.model.Admin
    username = "meow123"
    password = "123@C@t"
    new_password = "C@t__me0w"
    db.session.add(user_model(
        username=username,
        password=password,
    ))
    db.session.commit()
    rv = client.post("/api/auth", data=json.dumps(dict(
        username=username,
        password=password
    )), content_type='application/json')
    jwt = json.loads(rv.data)
    rv = client.post("/api/change_password", data=json.dumps({
        "original_pass": password,
        "pass": new_password
    }), content_type='application/json', headers={'Authorization': jwt})
    assert user_model.query.filter_by(
        username=username).first().password == new_password
    assert rv.status_code == 200
