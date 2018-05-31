#encoding:utf-8
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db
from app import app
import MySQLdb

manager = Manager(app)
database = Manager()
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('db', MigrateCommand)
manager.add_command('runServer', Server(host='localhost', port=5000))
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('database',database)

@database.command
def create():
    mysqldb = MySQLdb.connect("localhost", app.config.get('DATEBASE_USERNAME'), app.config.get('DATEBASE_PASSWORD'),
                              charset='utf8')
    cursor = mysqldb.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS wspider DEFAULT CHARSET utf8 COLLATE utf8_general_ci;")

@database.command
def reload():
    mysqldb = MySQLdb.connect("localhost", app.config.get('DATEBASE_USERNAME'), app.config.get('DATEBASE_PASSWORD'),
                              charset='utf8')
    cursor = mysqldb.cursor()
    cursor.execute("DROP DATABASE IF EXISTS wspider")
    cursor.execute("CREATE DATABASE IF NOT EXISTS wspider DEFAULT CHARSET utf8 COLLATE utf8_general_ci;")
    db.create_all()

if __name__ == '__main__':
    manager.run()