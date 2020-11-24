from datetime import datetime
from blog import db


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	content = db.Column(db.Text, nullable=False)
	email = db.Column(db.String(120), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.now)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

	def __repr__(self):
		return f"Comment({self.id}, '{self.title}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	content = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.now)
	tags = db.relationship('Tag', secondary=tags, lazy='subquery', 
							backref=db.backref('posts', lazy=True))
	cat_id = db.Column(db.Integer, db.ForeignKey('category.id'), 
						nullable=False)
	comments = db.relationship('Comment', backref='post', lazy=True)
	views = db.Column(db.Integer, default=0)

	def __repr__(self):
		return f"Post({self.id}, '{self.title}')"


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False, unique=True)
	posts = db.relationship('Post', backref='category', lazy=True)

	def __repr__(self):
		return f"Category({self.id}, '{self.title}')"


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False, unique=True)

	def __repr__(self):
		return f"Tag({self.id}, '{self.title}')"