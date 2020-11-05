from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	username=StringField('Username',validators=[DataRequired(), Length(min=2, max=255)])
	email=StringField('Email',validators=[DataRequired(),Email()])
	password=PasswordField('Password',validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit= SubmitField('Sign Up')


class LoginForm(FlaskForm):
	email=StringField('Email',validators=[DataRequired(),Email()])
	password=PasswordField('Password',validators=[DataRequired()])
	remember=BooleanField('Remember Me')
	submit= SubmitField('Sign In')

class SubscribersForm(FlaskForm):
	user_id=IntegerField('User Id',validators=[DataRequired()])
	plan_id=IntegerField('Plan id',validators=[DataRequired()])
	amount_payable=IntegerField('Amount Payable',validators=[DataRequired()])
	date_Of_call=StringField('Date Of Call',validators=[DataRequired()])
	call_duration=IntegerField('Call Duration',validators=[DataRequired()])
	submit= SubmitField('Submit')

class MonthlyForm(FlaskForm):
	user_id=IntegerField('User Id',validators=[DataRequired()])
	plan_id=IntegerField('Plan id',validators=[DataRequired()])
	monthly_bill=IntegerField('Monthly Bill', validators=[DataRequired()])
	submit= SubmitField('Submit')
