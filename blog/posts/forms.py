from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, SelectField, MultipleFileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email


class CommentForm(FlaskForm):
	name = StringField('name', validators=[
											DataRequired(), 
											Length(min=2, max=50)])
	email = EmailField('email', validators=[
											DataRequired(), 
											Email()])
	content = TextAreaField('content', validators=[
											DataRequired(), 
											Length(min=10, max=500)])
	submit = SubmitField('submit')


class PostForm(FlaskForm):
	title = StringField('title')
	content = TextAreaField('content')
	tags = StringField('tags')
	category = SelectField('category')
	file = MultipleFileField('files')
	submit = SubmitField('submit')


class CategoryForm(FlaskForm):
	title = StringField('title', validators=[DataRequired()])
	submit = SubmitField('submit')