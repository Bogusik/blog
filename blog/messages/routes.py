from blog import db, months, posts_per_page
from blog.messages.models import Message
from blog.messages.forms import MessageForm
from blog.posts.models import Category
from flask import render_template, redirect, url_for, Markup, flash, Blueprint, request
from flask_login import login_required

messages = Blueprint("messages", __name__)

@messages.route('/messages/')
@messages.route('/messages/<int:page>')
@login_required
def msgs(page=1):
	ms = Message.query.order_by(Message.id.desc()).\
			paginate(page=page, per_page=posts_per_page)
	return render_template	(
								'messages.html', 
								title="Повідомлення", 
								categories=Category.query.all(),
								messages=ms, 
								months=months
							)

@messages.route('/messages/delete')
@login_required
def delete(page=1):
	nx = request.args.get('next')
	message = Message.query.get(request.args.get('message'))
	if message:
		db.session.delete(message)
		db.session.commit()
	return redirect(nx if nx else url_for('messages.msgs'))


@messages.route('/contact', methods=['GET', 'POST'])
def contact():
	form = MessageForm()
	if form.validate_on_submit():
		name, email, content = (
									Markup.striptags(form.name.data), 
									Markup.striptags(form.email.data), 
									Markup.striptags(form.content.data)
								)
		db.session.add(Message(title=name, email=email, content=content))
		db.session.commit()
		s = f'Дякую, {Markup.striptags(form.name.data)}, за повідомлення :)'
		flash(s, 'success')
		return redirect(url_for('messages.contact'))
	elif form.is_submitted():
		flash("Будь ласка, заповніть всі поля відповідно до вимог.", "error")
	return render_template	(
								"contact.html", 
								categories=Category.query.all(),
								title="Напиши мені", 
								form=form
							)
