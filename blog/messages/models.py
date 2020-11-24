from datetime import datetime
from blog import db


class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	email = db.Column(db.String(120), nullable=False)
	content = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.now)
	
	def __repr__(self):
		return f"Message({self.id}, '{self.title}')"