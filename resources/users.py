from flask_restful import Resource, reqparse

from models.user import User


#class that will have an endpoint (/register)
class registerUser(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("username", type= str, required= True, help= "Leave no empty space")
	parser.add_argument("password", type= str, required= True, help= "Leave no empty space")

	def post(self):
		requestedData = self.parser.parse_args()
		if User.find_by_username(requestedData["username"]): #OR if user is not None, means we find something, so it´s repeated
			return {"message":"the user {} already exists".format(requestedData["username"])}, 400

		user = User(**requestedData)
		user.saveToDB()

		return user.json(), 201

	def delete(self):
		requestedData = self.parser.parse_args()
		if User.find_by_username(requestedData["username"]):
			User.deleteFromDB()
			return {"message":"user {} is now deleted".format(requestedData["username"])}
		else:
			return {"message":"user {} was not found".format(requestedData["username"])}

class UserList(Resource):
	def get(self):
		return {"users":[user.json() for user in User.query.all()]}


