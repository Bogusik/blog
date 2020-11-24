from flask import Blueprint, render_template
from blog.posts.models import Category, Post, Tag
from flask_login import login_required


admin = Blueprint('admin', __name__)


@admin.route('/stats')
@login_required
def stats():
	posts = Post.query.order_by(Post.views.desc()).all()
	views = sum([x.views for x in posts]) if posts else 0
	
	views_by_cat = []
	views_by_tag = []

	for tag in Tag.query.all():
		views_by_tag.append((tag, sum([x.views for x in Post.query.filter(Post.tags.contains(tag)).all()])))

	for cat in Category.query.all():
		views_by_cat.append((cat, sum([x.views for x in cat.posts])))

	return render_template	(
								"statistics.html",
								categories=Category.query.all(), 
								posts=posts,
								sum=views,
								views_by_cat=views_by_cat,
								views_by_tag=views_by_tag
							)