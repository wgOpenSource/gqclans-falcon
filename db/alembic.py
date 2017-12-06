import os

from alembic.config import Config

from config import config

alembic_config = Config()
alembic_config.set_main_option('url', config.db.master)
alembic_config.set_main_option('script_location', os.path.join(config.project_dir, 'db', 'migrations'))
alembic_config.set_main_option('file_template', '%%(year)d-%%(month).2d-%%(day).2d_%%(rev)s_%%(slug)s')
