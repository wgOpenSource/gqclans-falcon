import json
from unittest import TestCase

from alembic import command
from sqlalchemy_utils import database_exists, drop_database, create_database
from werkzeug.test import Client

from app import app
from db import db_factory
from db.alembic import alembic_config
from db.models import Base


def prepare_database():
    session = db_factory(master=True)
    bind = session.get_bind()

    if database_exists(bind.url):
        drop_database(bind.url)

    create_database(bind.url)

    session.close()

    command.upgrade(alembic_config, 'head')


class TestSession:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.session.autocommit:
            self.session.commit()
        else:
            self.session.flush()


class ResponseWrapper:
    status = None
    raw_response = None
    body = {}
    headers = None

    def __init__(self, app_iter, status, headers):
        self.status = status
        self.raw_response = list(app_iter)
        self.headers = dict(headers)

        try:
            self.status_code = int(status.split(None, 1)[0])
        except (KeyError, TypeError, ValueError):
            self.status_code = 0

        if self.raw_response:
            self.body = json.loads(self.raw_response[0])


class BaseTestCase(TestCase):
    MASTER_SESSION = None
    FACTORY_USE_MASTER_SESSION = True

    @classmethod
    def setUpClass(cls):
        cls.client = Client(
            app,
            response_wrapper=ResponseWrapper,
        )
        cls.MASTER_SESSION = db_factory(
            master=True,
            autoflush=False,
            autocommit=True,
            expire_on_commit=False,
        )
        cls.maxDiff = None

    @classmethod
    def tearDownClass(cls):
        cls.MASTER_SESSION.close()

    @property
    def db(self):
        return self.MASTER_SESSION

    def commit_after(self):
        return TestSession(self.db)

    def tearDown(self):
        for subclass in Base.__subclasses__():
            self.db.query(subclass).delete()
