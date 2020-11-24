from blog import db, bcrypt, posts_per_page
from flask import render_template, redirect, url_for, flash, abort
from blog.users.forms import AddUserForm, LoginForm
from blog.users.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask import Blueprint

users = Blueprint('users', __name__)

@users.route('/users', methods=['GET', 'POST'])
@users.route('/users/<int:page>', methods=['GET', 'POST'])
@login_required
def main(page=1):
	form = AddUserForm()

	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.passwd.data)
		user = User(
					name=form.name.data, 
					surname=form.surname.data, 
					username=form.username.data.lower(), 
					passwd=hashed_pw
					)
		db.session.add(user)
		db.session.commit()
		flash(f'Користувача додано', 'success')
		return redirect(url_for('users.main'))
	elif form.is_submitted():
		flash("Будь ласка, заповніть всі поля відповідно до вимог.", "error")

	return render_template(
							"users.html", 
							title="Додати крристувача", 
							form=form, 
							users=User.query.order_by(User.id.desc()).\
									paginate(page=page, per_page=posts_per_page)
						)

@users.route('/login/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('posts.main'))

	form = LoginForm()
	
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.passwd, form.passwd.data):
			login_user(user)
			return redirect(url_for('posts.main'))
		else:
			flash("Не вдалося ввійти!", "error")

	return render_template("login.html", title="Вхід", form=form)

@users.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('posts.main'))
