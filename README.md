## GQClans

### Description

A simple project that provides a GraphQL API, proxies requests and responses from/to Wargaming Public API
(https://developers.wargaming.net/) and stores some information in internal DB.

Backend project only, no frontend. Uses Falcon (https://falconframework.org/) as a main framework,
SQLAlchemy (http://www.sqlalchemy.org/) as ORM.

### Quickstart

Clone this project from Git repo. Activate virtualenv and install python packages (Python 3.6 is required):

    $ mkvirtualenv gqclans-falcon -p /usr/local/bin/python3.6
    (gqclans-falcon) $ pip install -r requirements.txt

Copy `infrastructure.py` and `testing.py` from examples and alter this file according your local settings:

    (gqclans-falcon) $ cp etc/config_example_infrastructure.py config_layers/infrastructure.py
    (gqclans-falcon) $ cp etc/config_example_testing.py config_layers/testing.py

Specify correct DB connection settings, create database and start scheme migration:

    (gqclans-falcon) $ inv db.upgrade

Start developer server:

    (gqclans-falcon) $ inv dev.runserver --host='localhost' --port=8014

Test that everything is OK:

    $ curl -XGET 'http://localhost:8014/graphql?query=\{ping\}' | pp
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100    22  100    22    0     0    187      0 --:--:-- --:--:-- --:--:--   188
    {
        "data": {
            "ping": "ok"
        }
    }

Run tests:

    (gqclans-falcon) $ inv dev.test --failfast


### DB tools guide

In order to create scheme migration use `alembic` tool:

    (gqclans-falcon) $ inv db.migration "Foo migration"
    Generating src/db/migrations/versions/2017-04-12_29a426db0e65_foo_migration.py ... done

To apply migration(s):

    (gqclans-falcon) $ inv db.upgrade

To rollback migration(s):

    (gqclans-falcon) $ inv db.downgrade

To view hash of last applied migration:

    (gqclans-falcon) $ inv db.current
    29a426db0e65 (head)

To view history range of applied migrations:

    (gqclans-falcon) $ inv db.history 29a426db0e65:
    <base> -> 29a426db0e65 (head), Foo migration

For each command you can get more detailed help:

    (gqclans-falcon) $ inv --help db.history
    Usage: inv[oke] [--core-opts] db.history [--options] [other tasks here ...]

    Docstring:
      List changeset scripts in chronological order.

      Usage:
          history -r[start]:[end]
          history -rqw42se:qa234    Show information from start to end revisions.
          history -r-3:             Show information from three revs ago up to head.
          history -r-2:current      Show information from two revs ago up to current revision.

    Options:
      -r STRING, --range=STRING   Revisions range like [start]:[end].

