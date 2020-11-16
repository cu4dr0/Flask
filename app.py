import os


from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.users import registerUser, UserList 
from resources.items import Items, ItemList
from resources.stores import Stores, StoreList

from datetime import timedelta

from db import db

app = Flask(__name__)
app.secret_key = "lordericktodopoderosocreadordeloscielosymares" 

app.config['JWT_AUTH_URL_RULE'] = '/login' #changes the "auth" endpoint for "login"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)# config JWT to expire within half an hour
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'# config JWT auth key name to be 'email' instead of default 'username'

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db' #can be any sqler such as mysql and just use the name of the database
#in my case is "data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #needed for not keeping track for unsaved data

jwt = JWT(app, authenticate, identity)

@app.before_first_request
def createTables():
	db.create_all()


api = Api(app)
api.add_resource(Items, "/item/<string:name>")
api.add_resource(Stores, "/store/<string:name>")

api.add_resource(ItemList, "/items")
api.add_resource(UserList,"/users")
api.add_resource(StoreList,"/stores")

api.add_resource(registerUser, "/register")



if __name__ == "__main__": 
	db.init_app(app)
	app.run(port = 5000, debug= True)