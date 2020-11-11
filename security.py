#this worsks as a databases

from resources.users import User

#users = [User("Juan", "asdf", "1")]

#usernameMapping = {us.name: us for us in users}#dictionary for finding a user by it's name quicker
#useridMapping = {us.id: us for us in users} #dictionary for finding a user byt it's id quicker

def authenticate(username, password):
	user = User.find_by_username(username) 
	if user and password == user.password: #OR if user is not None OR if user != None
		return user

def identity(payload):
	userid = payload["identity"]
	return User.find_by_id(userid)