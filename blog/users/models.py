from blog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	surname = db.Column(db.String(120), nullable=False)
	username = db.Column(db.String(120), nullable=False, unique=True)
	passwd = db.Column(db.String(120), nullable=False)

	def __repr__(self):
		return f"User({self.id}, '{self.name}')"
