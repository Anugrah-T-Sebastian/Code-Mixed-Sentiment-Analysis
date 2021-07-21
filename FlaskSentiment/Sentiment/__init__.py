from flask_sqlalchemy import SQLAlchemy   
from flask import Flask, render_template
from flask_bcrypt import Bcrypt   
from flask_login import LoginManager   

app = Flask(__name__)     
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Market.db'
app.config['SECRET_KEY'] = 'd770946afb62e547ecb834a6'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    

db = SQLAlchemy(app)        
bcrypt = Bcrypt(app)       

login_manager = LoginManager(app)       
login_manager.login_view = "login_page"    
login_manager.login_message_category = "info"       

from Sentiment import routes