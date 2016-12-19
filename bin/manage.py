#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

from unravelr import create_app
from flask_script import Manager, Shell, Server

app = create_app()

manager = Manager(app)
manager.add_command("shell", Shell(make_context=lambda: dict(app=app)))
manager.add_command("runserver", Server(port=app.config['PORT']))
manager.add_command("publicserver", Server(port=app.config['PORT'], host="0.0.0.0"))


if __name__ == "__main__":
    manager.run()
