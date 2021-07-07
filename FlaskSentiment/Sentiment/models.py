from Sentiment import db, login_manager
from Sentiment import bcrypt
from flask_login import UserMixin       #Provide extra methods required by flask for login system
                                        #Read more about it on https://flask-login.readthedocs.io/en/latest/#how-it-works

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable = False)
    email_address = db. Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:      #To display the commans in the digits
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f"${self.budget}"
    
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)       #Checks if the attempted password hash value to is equal to the stored Hash value



class Item(db.Model):       #Creating Database table schema
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length = 30), nullable = False, unique = True)
    company = db.Column(db.String(length = 12), nullable = True, unique = False)
    description = db.Column(db.String(length = 1024), nullable = False, unique = False)
    path = db.Column(db.String(length = 1024), nullable = False, unique = False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):      #magic function to create your own IDs of DB items
        return f'Item {self.name}'

    
    

