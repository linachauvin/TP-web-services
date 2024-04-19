from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask
from faker import Faker
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:root@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from flask import jsonify

@app.route('/users', methods=['GET'])
def get_users():
    users_list = users.query.all()
    user_data = []
    for user in users_list:
        user_data.append({
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'age': user.age,
            'email': user.email,
            'job': user.job
        })
    return jsonify(user_data)

@app.route('/applications', methods=['GET'])
def get_applications():
    applications_list = Application.query.all()
    app_data = []
    for app in applications_list:
        app_data.append({
            'id': app.id,
            'appname': app.appname,
            'username': app.username,
            'lastconnection': app.lastconnection.isoformat(),
            'user_id': app.user_id
        })
    return jsonify(app_data)
    
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    job = db.Column(db.String(100))
    applications = db.relationship('Application', backref='user', lazy=True)

    def __init__(self, firstname, lastname, age, email, job):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.email = email
        self.job = job

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    lastconnection = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, appname, username, lastconnection=None, user_id=None):
        self.appname = appname
        self.username = username
        self.lastconnection = lastconnection
        self.user_id = user_id

fake = Faker()

def populate_tables():
    apps = ["Facebook", "Instagram", "TikTok", "Twitter"]
    for _ in range(100):
        firstname = fake.first_name()
        lastname = fake.last_name()
        age = random.randrange(18, 50)
        email = fake.email()
        job = fake.job().replace("'", "")
        user = users(firstname=firstname, lastname=lastname, age=age, email=email, job=job)
        db.session.add(user)
        db.session.commit()

        user_id = user.id
        appname = random.choice(apps)
        username = fake.user_name()
        lastconnection = fake.date_time_between(start_date='-1y', end_date='now')
        application = Application(appname=appname, username=username, lastconnection=lastconnection, user_id=user_id)
        db.session.add(application)

if __name__ == "__main__":
    with app.app_context():
        populate_tables()

app.run(host="0.0.0.0", port=8081, debug=True)