import os
from logging import getLogger

from invoke import task

logger = getLogger(__name__)


@task(help={
    'host': 'Host to run server on',
    'port': 'Port to run server on',
})
def runserver(ctx, host='127.0.0.1', port=8000):
    """
    Starts development server

    Usage:
        inv dev.runserver --host='localhost' --port=8000
    """
    from werkzeug.serving import run_simple

    from app import app

    subquote = 'Reloading' if 'WERKZEUG_RUN_MAIN' in os.environ else 'Starting'
    print(f'{subquote} development server at http://{host}:{port} ...')

    run_simple(host, port, app, use_reloader=True)


@task(help={
    'paths': 'Paths to search tests',
    'verbose': 'TestResult verbosity',
    'failfast': 'Stops on the first test fail',
    'skip_coverage': 'Skips coverage reporting',
})
def test(ctx, paths='', failfast=False, verbose=False, skip_coverage=False):
    """
    Runs the unit tests

    Usage:
        inv dev.test --paths='api' --failfast
    """
    import unittest

    import nose
    from coverage import Coverage
    from nose.plugins.capture import Capture
    from nose.plugins.logcapture import LogCapture

    from config import set_config
    config = set_config('testing')

    from tests import prepare_database as tests_prepare_database

    class ConfiguringPlugin(nose.plugins.Plugin):
        enabled = True

        def configure(self, options, conf):
            pass

        def begin(self):
            tests_prepare_database()

    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    argv = ['nosetests']

    if failfast:
        argv.append('--stop')

    for path in paths.split(','):
        prefix = 'tests.'
        if not path:
            prefix = prefix[:-1]

        argv.append(prefix + path)

    plugins = [ConfiguringPlugin()]

    if config.nose.log_capturing:
        argv += [
            '--logging-clear-handlers',
            '--logging-format=(%(thread)d) %(name)s: %(levelname)s: %(message)s'
        ]
        plugins.append(LogCapture())

    if config.nose.stdout_capturing:
        plugins.append(Capture())

    os.chdir(os.path.join(config.project_dir, os.path.pardir))

    if not skip_coverage:
        cov = Coverage(
            source=[config.project_dir],
            omit=[
                'src/admin/*',
                'src/celery_tasks/*',
                'src/db/*',
                'src/tasks/*',
                'src/tests/*',
            ],
        )
        cov.start()

    nose.main(
        argv=argv,
        testRunner=runner,
        plugins=plugins,
        exit=False,
    )

    if not skip_coverage:
        directory = os.path.join(config.project_dir, '.coverage_report')
        print(f'\nSaving coverage report to "{os.path.abspath(directory)}"\n')

        cov.stop()
        cov.save()
        cov.html_report(directory=directory, title='WSP Coverage Report')


@task
def prepare_database(ctx):
    """
    Drops schema of the current database and creates the new one with applied migrations. Designed for test running
    purpose only.

    Usage:
        inv dev.prepare_database
    """

    from config import set_config
    set_config('testing')

    from tests import prepare_database
    prepare_database()
