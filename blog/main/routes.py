from flask import Blueprint, render_template
from blog.posts.models import Category


main = Blueprint('main', __name__)


@main.route('/about')
def about():
	return render_template("about.html", categories=Category.query.all())
