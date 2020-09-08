from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers
from balmid.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email exists, Try logging in')


    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
            
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
        try:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError

        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('This number is already registered, try another one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email exists, Try another')


    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            try:
                p = phonenumbers.parse(phone.data)
                if not phonenumbers.is_valid_number(p):
                    raise ValueError()
                
            except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
                raise ValidationError('Invalid phone number')
            try:
                user = User.query.filter_by(phone=phone.data).first()
                if user:
                    raise ValidationError

            except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
                raise ValidationError('This number is already registered, try another one.')


class PorfolioForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=20)])
    product_code = StringField('Product Code', validators=[DataRequired(), Length(min=2, max=20)])
    units = IntegerField('Units', validators=[DataRequired()])
    amount_per_unit = IntegerField('Amount Per Unit', validators=[DataRequired()])
    interest_rate = IntegerField('Interest Rate (%)', validators=[DataRequired()])
    duration = IntegerField('Duration (Days)', validators=[DataRequired()])
    submit = SubmitField('Save Portfolio')