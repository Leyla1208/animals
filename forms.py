from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class Main(FlaskForm):
    pass


class RegistrationForm(FlaskForm):
    login = StringField('Имя пользователя:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    check_password = PasswordField('Повторите пароль:',
                                   validators=[EqualTo(fieldname='password', message='Пароли должны совпадать!')])
    submit = SubmitField('Зарегистрироваться')


class Profile(FlaskForm):
    pass


class SettingsForm(FlaskForm):
    login = StringField('Имя:')
    password = PasswordField('Пароль:')
    check_password = PasswordField('Повторите пароль:',
                                   validators=[EqualTo(fieldname='password', message='Пароли должны совпадать!')])
    submit = SubmitField('Изменить')


class Dogs(FlaskForm):
    pass


class AddPet(FlaskForm):
    pet_name = StringField('Имя питомца: ', validators=[DataRequired()])
    age = IntegerField("Возраст питомца: ", validators=[DataRequired()])
    type = StringField("Вид: ", validators=[DataRequired()])
    poroda = StringField("Порода: ", validators=[DataRequired()])
    submit = SubmitField('Добавить питомца')


class AddFeedback(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание: ", validators=[DataRequired()])
    submit = SubmitField('Добавить отзыв')


class Birds(FlaskForm):
    pass


class Cats(FlaskForm):
    pass


