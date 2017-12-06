from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_session


class BaseModel:
    @property
    def session(self):
        return object_session(self)


metadata = MetaData()
class_registry = {}
Base = declarative_base(class_registry=class_registry, cls=BaseModel, metadata=metadata)

# pylint: disable = wrong-import-position
# flake8: noqa
