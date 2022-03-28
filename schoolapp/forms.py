from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator
from schoolapp.models import User


class InsertForm(FlaskForm):
    full_name = StringField('Имя, Фамилия',
                           validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    grade = IntegerField("Класс", validators=[DataRequired()])
    date_of_birth = StringField("Дата рождения", validators=[DataRequired()])
    address = StringField("Адрес", validators=[DataRequired()])
    phone_number = StringField("Телефонный номер", validators=[DataRequired()])
    tuition_fee = StringField("Плата за обучение")
    additional_info = StringField("Дополнительная информация")
    gender = StringField("Пол")
    active = IntegerField("Active")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Этот почтовый адрес занят. Пожалуйста выберите другой.")


class RegistrationForm(FlaskForm):
    full_name = StringField('Имя, Фамилия',
                           validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired(), EqualTo('password')])
    grade = IntegerField("Класс", validators=[DataRequired()])
    phone_number = StringField("Телефонный номер", validators=[DataRequired()])
    tuition_fee = StringField("Плата за обучение")
    additional_info = StringField("Дополнительная информация")
    gender = StringField("Пол")
    date_of_birth = StringField("Дата рождения", validators=[DataRequired()])
    address = StringField("Адрес", validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Этот почтовый адрес занят. Пожалуйста выберите другой.")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    full_name = StringField('Имя, Фамилия', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    grade = IntegerField("Класс", validators=[DataRequired()])
    date_of_birth = StringField("Дата рождения", validators=[DataRequired()])
    phone_number = StringField("Телефонный номер", validators=[DataRequired()])
    tuition_fee = StringField("Плата за обучение")
    additional_info = StringField("Дополнительная информация")
    gender = StringField("Пол")
    address = StringField("Адрес", validators=[DataRequired()])
    picture = FileField("Обновить фото", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField('Обновить профиль')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Этот почтовый адрес занят. Пожалуйста выберите другой.")

