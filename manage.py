#!/usr/bin/env python

import os
from ReBloger import create_app, db
from ReBloger.general.models import Post, Navigation, Category, Tag
from ReBloger.manager.models import Author
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app('dev')
manager = Manager(app)
migrate = Migrate(app, db)


def init_with_data():
    Navigation.generate()
    Category.generate()
    Tag.generate()
    Author.generate()
    Post.generate()


def make_shell_context():
    return dict(app=app, db=db, Author=Author, Post=Post, Category=Category, Navigation=Navigation, init_data=init_with_data)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()