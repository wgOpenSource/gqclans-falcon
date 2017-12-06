from logging import getLogger

from alembic import command
from invoke import task

logger = getLogger(__name__)


@task
def current(ctx):
    """
    Get current migration.
    """
    from db.alembic import alembic_config

    command.current(alembic_config)


@task(help={
    'range': 'Revisions range like [start]:[end].',
})
def history(ctx, range_):
    """
    List changeset scripts in chronological order.

    Usage:
        history -r[start]:[end]
        history -rqw42se:qa234    Show information from start to end revisions.
        history -r-3:             Show information from three revs ago up to head.
        history -r-2:current      Show information from two revs ago up to current revision.
    """
    from db.alembic import alembic_config

    command.history(alembic_config, rev_range=range_)


@task(help={
    'revision': 'Revision id eg. 38cr251a7 of "head" (default: head).',
})
def upgrade(ctx, revision='head'):
    """
    Upgrade to later revision.
    Usage:
        upgrade -r 38cr251a7     Will upgrade to revision 38cr251a7.
        upgrade                  Will upgrade to head.
    """
    from db.alembic import alembic_config

    command.upgrade(alembic_config, revision)


@task(help={
    'revision': 'Revision id eg. 38cr251a7 or "base" (default: -1).',
})
def downgrade(ctx, revision='-1'):
    """
    Reverts to a revision.
    Usage:
        downgrade --revision=38cr251a7   Downgrade to revision 38cr251a7.
        downgrade             Downgrade to previous revision.
    """
    from db.alembic import alembic_config

    command.downgrade(alembic_config, revision)


@task
def branches(ctx):
    """
    Show current un-spliced branch points.
    Usage:
        branches
    """
    from db.alembic import alembic_config

    command.branches(alembic_config)


@task(help={
    'message': 'The revision message.'
})
def migration(ctx, message):
    """
    Creates a new revision file.
    Usage:
        migration -m SOME_MESSAGE
    """
    from db.alembic import alembic_config

    command.revision(alembic_config, message=message, autogenerate=True)


@task(help={
    'first': 'Current revision id eg. 38cr251a7',
})
def showsql(ctx, first):
    """
    Show what migration will be applied (in SQL).
    Usage:
        showsql -f 38cr251a7
    """
    from db.alembic import alembic_config

    command.upgrade(alembic_config, f'{first}:head', sql=True)


@task
def shell(ctx, extra_command=None):
    """
    Runs the database shell for master DB.
    Usage:
        inv db.shell
        inv db.shell --extra-command='SELECT id FROM clans;'
    """
    from urllib.parse import urlparse
    from config import config

    db_options = urlparse(config.db.master)
    command = 'PGPASSWORD={password} PGCLIENTENCODING="UTF-8" psql -h {host} -U {user} {name}'
    if db_options.port:
        command += ' -p {port}'

    if extra_command:
        command += ' -c "{extra_command}"'

    ctx.run(command.format(
        name=db_options.path.replace('/', ''),
        host=db_options.hostname,
        port=db_options.port,
        user=db_options.username,
        password=db_options.password,
        extra_command=extra_command,
    ), pty=True)
