from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config
from db.session import SessionManager, build_session_context_manager

engines = {
    'master': create_engine(
        config.db.master,
        pool_size=config.db.pool_size,
        max_overflow=config.db.max_overflow,
    ),
    'slaves': [
        create_engine(
            slave,
            pool_size=config.db.pool_size,
            max_overflow=config.db.max_overflow,
            isolation_level='AUTOCOMMIT',
        )
        for slave in config.db.slaves or [config.db.master]
    ]
}

db_factory = sessionmaker(class_=SessionManager, engines=engines)

master_session = build_session_context_manager(
    db_factory,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
