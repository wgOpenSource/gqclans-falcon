from invoke import Collection

import tasks.dev as dev_tasks
import tasks.db as db_tasks

ns = Collection()
ns.add_collection(Collection.from_module(dev_tasks))
ns.add_collection(Collection.from_module(db_tasks))
