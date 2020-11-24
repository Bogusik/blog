from blog import db, months, posts_per_page
from blog.posts.models import Category, Tag, Post, Comment
from blog.users.models import User
from flask import Blueprint, render_template, redirect, url_for, Markup, flash, abort, request
from blog.posts.forms import PostForm, CommentForm, CategoryForm
from flask_login import login_required
from blog.posts.utils import *
from sqlalchemy import func
import shutil

posts = Blueprint('posts', __name__)

@posts.route('/')
@posts.route('/page/<int:page>')
def main(page=1):
	posts = Post.query.order_by(Post.id.desc()).\
				paginate(page=page, per_page=posts_per_page)
	return render_template	(
								'posts.html',
								title="Головна сторінка", 
								categories=Category.query.all(), 
								url="page", 
								posts=posts,
								months=months
							)

@posts.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
	if post := Post.query.get(id):
		post.views += 1
		db.session.commit()
		form = CommentForm()
		if form.validate_on_submit():
			name, email, content = 	(
										Markup.striptags(form.name.data), 
										Markup.striptags(form.email.data), 
										Markup.striptags(form.content.data)
									)
			db.session.add(Comment(title=name, email=email, 
									content=content, post_id=id))
			db.session.commit()
			s = f'Дякую, {Markup.striptags(form.name.data)}, за коментар :)'
			flash(s, 'success')
			return redirect(url_for('posts.post', id=id))
		elif form.is_submitted():
			flash("Будь ласка, заповніть всі поля відповідно до вимог.", 
					"error")
		related_posts = Post.query.filter_by(cat_id=post.cat_id).limit(5)
		return render_template	(
									'post.html', 
									title=post.title, 
									categories=Category.query.all(), 
									post=post, 
									months=months, 
									form=form,
									related_posts=related_posts
								)
	else:
		return redirect(url_for('posts.main'))

@posts.route('/category/<int:cat>/')
@posts.route('/category/<int:cat>/<int:page>')
def category(cat, page=1):
	if (category := Category.query.get(cat)):
		posts = Post.query.filter_by(cat_id=cat).order_by(Post.id.desc()).\
					paginate(page=page, per_page=posts_per_page)
		return render_template	(
									'posts.html', 
									categories=Category.query.all(),
									url = "category/" + str(cat),
									title=category.title, 
									posts=posts, 
									months=months
								)
	else:
		abort(404)

@posts.route('/categories',  methods=['GET', 'POST'])
@posts.route('/categories/<int:page>',  methods=['GET', 'POST'])
@login_required
def categories(page=1):
	form = CategoryForm()
	if form.validate_on_submit():
		if not Category.query.filter_by(title=form.title.data).first():
			db.session.add(Category(title=form.title.data))
			db.session.commit()
		else:
			flash("Розділ вже існує!", "error")
	elif form.is_submitted():
		flash("Введіть назву категорії!", "error")
	return render_template	(
								'categories.html', 
								categories=Category.query.all(),
								categors=Category.query.\
											order_by(Category.id.desc()).\
											paginate(
												page=page, 
												per_page=posts_per_page
												),
								title="Категорії", 
								form=form
							)

@posts.route('/tag/<int:tag>/')
@posts.route('/tag/<int:tag>/<int:page>')
def tag(tag, page=1):
	if (tagg := Tag.query.get(tag)):
		posts = Post.query.filter(Post.tags.contains(tagg)).\
					order_by(Post.id.desc()).\
						paginate(page=page, per_page=posts_per_page)
		return render_template	(
									'posts.html', 
									categories=Category.query.all(), 
									url = "tag/" + str(tag),
									title="#"+tagg.title, 
									posts=posts, 
									months=months
								)
	else:
		return redirect(url_for('posts.main'))


@posts.route('/post/add', methods=['GET', 'POST'])
@login_required
def post_add():
	form = PostForm()
	form.category.choices = [(str(c.id), c.title) for c in Category.query.all()]
	
	if form.validate_on_submit():
		tags = conformTags(form)

		post = Post (
						title=form.title.data, 
						content=form.content.data, 
						tags=tags, 
						cat_id=form.category.data
					)
		post.content = post.content.replace("$$id", str(post.id))
		db.session.add(post)
		db.session.commit()

		uploadFiles(form, 
			os.getcwd() + "/blog/static/posts/" + str(post.id) + "/")

		flash(f'Пост було опубліковано', 'success')
		return redirect(url_for('posts.post_add'))
	elif form.is_submitted():
		flash("Користувач з таким логіном вже існує!", "error")

	return render_template	(
								"add_post.html",
								categories=Category.query.all(), 
								title="Додати пост", 
								form=form,
								files=[]
							)

@posts.route('/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def post_edit(id=1):
	form = PostForm()
	form.category.choices = [(str(c.id), c.title) for c in Category.query.all()]
	post = Post.query.get(id)

	if not post:
		abort(404)

	if form.validate_on_submit():
		post.title = form.title.data
		post.tags = conformTags(form)
		post.cat_id = form.category.data
		post.content = form.content.data.replace("$$id", str(post.id))
		db.session.commit()

		uploadFiles(form, 
			os.getcwd() + "/blog/static/posts/" + str(post.id) + "/")


		flash(f'Пост було опубліковано', 'success')
		return redirect(url_for('posts.post_edit', id=id))
	elif form.is_submitted():
		flash("Будь ласка, заповніть всі поля відповідно до вимог.", "error")
	form.title.data = post.title
	form.tags.data = ", ".join([tag.title for tag in post.tags])
	form.content.data = post.content
	return render_template	(
								"add_post.html", 
								title="Редагувати пост", 
								form=form,
								files=listFiles(os.getcwd() + "/blog/static/posts/" + str(post.id) + "/")
							)

@posts.route('/delete', methods=['GET', 'POST'])
@login_required
def delete(page=1):
	nx = request.args.get('next')
	if post := Post.query.get(request.args.get('post')):
		shutil.rmtree(os.getcwd() + '/blog/static/posts/' + str(post.id))
		db.session.delete(post)
		db.session.commit()
	if comment := Comment.query.get(request.args.get('comment')):
		db.session.delete(comment)
		db.session.commit()
	if category := Category.query.get(request.args.get('category')):
		for post in category.posts:
			db.session.delete(post)
		db.session.delete(category)
		db.session.commit()
	if user := User.query.get(request.args.get('user')):
		db.session.delete(User)
		db.session.commit()
	if file := request.args.get('file'):
		deleteFile(os.getcwd() + "/blog/static/posts/" + file)
	return redirect(nx if nx else url_for('posts.main'))