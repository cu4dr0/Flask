from db import db

class Item(db.Model):
	__tablename__ = "items"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision= 2))

	store_id = db.Column(db.Integer, db.ForeignKey("stores.id")) #the table
	store = db.relationship("Store") #the class name 
	def __init__(self, name, price, store_id):
		self.name = name
		self.price = price
		self.store_id = store_id

	def json(self):
		return {"name":self.name, "price":self.price}
	@classmethod
	def findByName(cls, name):
		return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE name = name LIMIT 1

	def saveToDB(self):
		db.session.add(self)
		db.session.commit()
		#db.session.close()

	def deleteFromDB(self):
		db.session.delete(self)
		db.session.commit()
		#db.session.close()