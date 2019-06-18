import os
import unittest

from blueprints import blueprint
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from main import db, create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
# app = create_app('test')
app.register_blueprint(blueprint, url_prefix='/api/v1')
app.app_context().push()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run(host='0.0.0.0', port=3000)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
