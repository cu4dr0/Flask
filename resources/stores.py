from flask_restful import Resource#, reqparse

from models.store import Store

class Stores(Resource):
	"""	parser = reqparse.RequestParser()
	parser.add_argument()"""
	def get(self, name):
		store = Store.findByName(name)
		if store:
			return store.json() #returns also a list of items
		return {"message":"store {} not found".format(name)}
	def post(self, name):
		if Store.findByName(name):
			return {"message":"a store with name {} already exists".format(name)},400
		store = Store(name)
		try:
			store.saveToDB()
		except:
			return {"message":"an error occurred while creating your store"},500
		return store.json(),201
	def delete(self, name):
		store = Store.findByName(name)
		if store:
			try:
				store.deleteFromDB()
				return {"message":"store {} was deleted".format(name)}
			except:
				return {"message":"an error occurred while deleting your store"},500
		return {"message":"store {} was not found".format(name)}

class StoreList(Resource):
	def get(self):
		return {"stores": [store.json() for store in Store.query.all()]}