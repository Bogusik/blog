from flask import Flask, template_rendered, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

posts_per_page = 10
months = [
			"січня","лютого","березня",
			"квітня","травня","червня",
			"липня","серпня","вересня",
			"жовтня","листопада","грудня"
		]

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def working(sender, **extra):
	from blog.admin.models import View
	db.session.add(View(link=request.path))
	db.session.commit()

def create_app(config="config.json"):
	app = Flask(__name__)
	app.config.from_json(config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	login_manager.login_view = 'users.login'
	login_manager.login_message = ''

	from blog.users.routes import users
	from blog.admin.routes import admin
	from blog.main.routes import main
	from blog.posts.routes import posts
	from blog.messages.routes import messages
	app.register_blueprint(users)
	app.register_blueprint(admin)
	app.register_blueprint(main)
	app.register_blueprint(posts)
	app.register_blueprint(messages)

	template_rendered.connect(working, app)

	return app


def create_db():
	from blog.users.models import User
	from blog.admin.models import View
	from blog.posts.models import tags, Comment, Post, Category, Tag
	from blog.messages.models import Message

	db.create_all()