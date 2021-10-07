from app import db
import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)    
    role = db.StringField(required=True, default='user')
    accounts = db.ListField(db.ReferenceField('Account'))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login.user_loader
def load_user(id):
    return User.objects.get(id = id)

class Account(db.Document):
    user = db.ReferenceField('User', required = True)
    coin = db.ReferenceField('Coin', required = True)
    balance = db.FloatField(required = True, min=0)

class Transaction(db.Document):
    fromAccount = db.ReferenceField('Account', required = True)
    toAccount = db.ReferenceField('Account', required = True)
    amount = db.FloatField(required = True, min=0)
    creation = db.DateTimeField(default = datetime.datetime.utcnow, required=True)

class Coin(db.Document):
    name = db.StringField(required=True, unique=True    ) 
    currency = db.StringField(required=True, unique=True)