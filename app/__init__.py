from flask import Flask
from flask_bootstrap import Bootstrap
import pymysql, os, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.static_folder = 'static'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

def credentials(db_input):
    with open(os.path.expanduser("/short/Credentials/Creds/Wonderfell/{}.json".format(db_input)), mode='r') as op:
        payload = json.load(op)
    return payload


profconn = pymysql.connect(host='127.0.0.1',
                        port=3306,
                        user=credentials("wonderfell_database")['uname'],
                        passwd=credentials("wonderfell_database")['passwd'],
                        db=credentials("wonderfell_database")['db'])

musiconn = pymysql.connect(host='127.0.0.1',
                        port=3306,
                        user=credentials("music_database")['uname'],
                        passwd=credentials("music_database")['passwd'],
                        db=credentials("music_database")['db'])

from app import routes
