# entrypoint of app
# The below script is a sample

import os
import unittest
from logging import getLogger

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.logging_config import setup_logger
from app.main.models import user

setup_logger()
LOG = getLogger(__name__)

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    LOG.info('initiating app...')
    app.run()

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
    	#return error code
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
