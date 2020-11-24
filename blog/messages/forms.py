from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email


class MessageForm(FlaskForm):
	name = StringField('name', validators=[	
											DataRequired(), 
											Length(min=2, max=64)])
	email = EmailField('email', validators=[
											DataRequired(), Email()])
	content = TextAreaField('content', validators=[
											DataRequired(), Length(min=50)])
	submit = SubmitField('submit')