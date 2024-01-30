from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
STRING_LENGTH = 128
ANSWER_LENGTH = 1024


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(STRING_LENGTH), index=True, unique=True)
    password_hash = db.Column(db.String(STRING_LENGTH))
    #is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    #confirmed_on = db.Column(db.DateTime, nullable=True)
    feedback = db.relationship('Feedback', backref='user', lazy='dynamic')
    download = db.relationship('Download', backref='user', lazy='dynamic')
    #donation = db.relationship('Donation', backref='user', lazy='dynamic')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f'<{self.email}>'

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    pluginName = db.Column(db.String(STRING_LENGTH))
    #download = db.relationship('Download', backref='user', lazy='dynamic')
    daw = db.Column(db.String(STRING_LENGTH))
    answer1 = db.Column(db.String(ANSWER_LENGTH))
    answer2 = db.Column(db.String(ANSWER_LENGTH))
    answer3 = db.Column(db.String(ANSWER_LENGTH))
    answer4 = db.Column(db.String(ANSWER_LENGTH))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<id:{self.id}, user_id:{self.user_id}, name:{self.name}, daw:{self.daw}, answer1:{self.answer1}, answer2:{self.answer2}, answer3:{self.answer3}, answer4:{self.answer4}>'
    

class Download(db.Model):
    id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    pluginName = db.Column(db.String(STRING_LENGTH), primary_key=True)
    version = db.Column(db.String(STRING_LENGTH))
    updateSignup = db.Column(db.Boolean, default = False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return f'<id:{self.id}, user_id:{self.user_id}, name:{self.pluginName} {self.version}, updateSignup:{self.updateSignup}>' 
    
'''
class Donation(db.Model):
    id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pluginName = db.Column(db.String(STRING_LENGTH), primary_key=True)
    version = db.Column(db.String(STRING_LENGTH))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    amount = db.Column(db.Float, default = 0) 
'''
class Plugin(db.Model):
    id = db.Column(db.Integer)
    name = db.Column(db.String(STRING_LENGTH), primary_key=True)
    #currentVersion = db.Column(db.String(STRING_LENGTH))
    #linkToPage