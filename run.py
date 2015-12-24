#!/usr/bin/env python
from app import create_app, db
from app.models import Alert, Restaurant
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
import os 

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Alert=Alert, Restaurant=Restaurant)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
