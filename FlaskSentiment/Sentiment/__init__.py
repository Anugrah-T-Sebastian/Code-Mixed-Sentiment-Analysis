from flask_sqlalchemy import SQLAlchemy     #importing header to synchronize database
from flask import Flask, render_template
from flask_bcrypt import Bcrypt     #To encrypt password into Hash values
from flask_login import LoginManager        #To manage Login functionalities



app = Flask(__name__)       #Creating flask instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Market.db'
app.config['SECRET_KEY'] = 'd770946afb62e547ecb834a6'      #SECRET KEY!! DO NOT LOOSE WHILE DEVELOPING

db = SQLAlchemy(app)        #Passing the flask instance to Database instance

bcrypt = Bcrypt(app)        #Passing the flask instance to Bcrypt instance

login_manager = LoginManager(app)       #Passing the flask instance to LoginMangaer instance
login_manager.login_view = "login_page"     #Providing route to Login page so that when
login_manager.login_message_category = "info"       #Message flashed with Blue color

from Sentiment import routes


#Username: admin
#Email: admin@admin.com
#Passowrd: admin@123

#agna
#agna@gmail.co
#