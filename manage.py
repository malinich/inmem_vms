from flask_script import Manager, Shell

from app import create_app

app = create_app()


def shell_context():
    return {"app": app}


manager: Manager = Manager(app)
manager.add_command('shell', Shell(make_context=shell_context))

if __name__ == '__main__':
    manager.run()

