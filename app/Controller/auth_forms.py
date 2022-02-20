from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length, Email
from app.Model.models import User

def check_wsu_email(form, field):
    if len(field.data) <= 8:
        raise ValidationError("Field must be at least 9 characters (must include @wsu.edu)")
    elif field.data[-8:] != "@wsu.edu":
        raise ValidationError("Field must be a valid wsu email.")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired(), Email(), check_wsu_email])
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField("Repeat Password", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_email(self, email):
        userEmail = User.query.filter_by(email=email.data).first()
        if userEmail is not None:
            raise ValidationError('The email already exists! Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign In")