from blog import db
from datetime import datetime


class View(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	link = db.Column(db.String(120), nullable=False)
	time = db.Column(db.DateTime, nullable=False, default=datetime.now)

	def __repr__(self):
		return f"Views({self.id}, '{self.link}')"
