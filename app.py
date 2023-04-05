from flask import send_file

from __init__ import create_app
from dbConn import getAreas

app = create_app()


if __name__ == '__main__':
    app.run()
