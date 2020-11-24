from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from blog.users.models import User


class AddUserForm(FlaskForm):
	name = StringField('title', validators=[DataRequired()])
	surname = StringField('content', validators=[DataRequired()])
	username = StringField('content', validators=[DataRequired()])
	passwd = PasswordField('content', validators=[DataRequired()])
	submit = SubmitField('submit')

	def validate_username(self, username):

		user = User.query.filter_by(username=username.data).first()

		if user:
			raise ValidationError("Користувач існує!")

class LoginForm(FlaskForm):
	username = StringField('content', validators=[DataRequired()])
	passwd = PasswordField('content', validators=[DataRequired()])
	submit = SubmitField('submit')