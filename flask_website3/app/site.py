import sys
import os
from app import app
from app import db
# from flask import request
# from app.mode import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

if __name__ == '__main__':
    app.run()
