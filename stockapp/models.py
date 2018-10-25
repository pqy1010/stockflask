import flask
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from . import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    password_hash=db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r'%self.username

class StockState(db.Model):
    __tablename__='stockstatus'
    ID=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    code=db.Column(db.Text)
    ctime=db.Column(db.Text)
    b_time=db.Column(db.Text)
    b_price= db.Column(db.Float)
    b_money=db.Column(db.Float)
    b_count=db.Column(db.Integer)
    owntime=db.Column(db.Float)
    state=db.Column(db.Text)
    earn=db.Column(db.Float)
    earnrate=db.Column(db.Float)
    s_price =db.Column(db.Float)
    s_time=db.Column(db.Text)

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
