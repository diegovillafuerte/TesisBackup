import os
from flask_script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from main import app, db


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()