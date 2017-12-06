from contextlib import contextmanager

from sqlalchemy.orm import Session


class SessionManager:
    """
    Class that will be passed to sqlalchemy.orm.sessionmaker
    """

    def __new__(cls, engines=None, master=True, **kwargs):
        kwargs['bind'] = engines['master']
        return Session(**kwargs)


def _db_session_raiser(*args, **kwargs):
    raise RuntimeError('Trying to use a session out of context')


def build_session_context_manager(session_factory, **kwargs):
    @contextmanager
    def master_session(**context):
        """
        Provide a transactional master database scope around a series of operations.

        :rtype: sqlalchemy.orm.Session
        """

        context = dict(kwargs, **context)
        master = session_factory(master=True, **context)

        try:
            yield master
            master.commit()
        except:
            master.rollback()
            raise
        finally:
            master.close()
            master.connection = _db_session_raiser

    return master_session
