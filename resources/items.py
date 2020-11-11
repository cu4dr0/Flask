from flask_restful import reqparse, Resource
import sqlite3 as sqlite 
from flask_jwt import jwt_required

from models.item import Item


#class that will have an endpoint (/item<string:name>)
class Items(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("price", type= float, required=True, help="This space cannot be blank")#parameters needed to work
	parser.add_argument("store_id", type= float, required=True, help="Use the store ID")
	@jwt_required()
	def get(self, name):
		item = Item.findByName(name)
		if item:
			return item.json()
		return {"message":"item {} not found".format(name)}

	def post(self, name):
		if Item.findByName(name):
			return {"message":"the item {} already exists".format(name)}, 400 
		requestedData = self.parser.parse_args()
		item = Item(name,**requestedData)#or requestedData["price"], requestedData["store_id"]

		try:
			item.saveToDB() #inserts itself
		except:
			return {"message":"Something went wrong with creating your item, try again later"}, 500 #500: internal server error

		return item.json(), 201 

	def delete(self, name):
		item = Item.findByName(name)
		if item:
			try:
				item.deleteFromDB()
				return {"message":"item {} deleted".format(name)}
			except:
				return {"message":"Something went wrong with deleting your item, try again later"}, 500 
		return {"message":"item {} was not found".format(name)}

	def put(self, name):
		requestedData = self.parser.parse_args()
		item = Item.findByName(name)

		if item: #if item is not None
			try:
				item.price = requestedData["price"]
				item.store_id = requestedData["store_id"]
			except:
				return {"message":"something went wrong with updating your existing item, try again later"},500
		else:
			try:
				item = Item(name,**requestedData)#or requestedData["price"], requestedData["store_id"]
			except:
				return {"message":"something went wrong with creating your new item, try again later"},500
		item.saveToDB()
		return item.json(),201


#class that will have an endpoint (/items)
class ItemList(Resource):
	def get(self):		
		return {"items": [item.json() for item in Item.query.all()]} #or list(map(lambda item: item.json(), Item.query.all()))
