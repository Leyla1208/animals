from flask import Flask, render_template, redirect, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource

from data.models import User, Pet, Feedback
from forms import LoginForm, RegistrationForm, AddFeedback, AddPet, SettingsForm, Main, Profile, Cats, Dogs, Birds

from data import db_session
db_session.global_init("database/profile_info.sqlite")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'animal_site'
login_manager = LoginManager(app)
login_manager.login_view = '/login'
api = Api(app)

#api.add_resource(feedbacks_resources.ListResource, '/api/v2/news')
#api.add_resource(feedbacks_resources.Resource, '/api/v2/news/<int:news_id>')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    return user


def abort_if_feedbacks_not_found(id):
    session = db_session.create_session()
    feedbacks = session.query(Feedback).get(id)
    if not feedbacks:
        abort(404, message=f"Отзыв {id} не найден.")


@app.route('/login', methods=['GET', 'POST'])
def sign_in_page():
    logout_user()
    message = ''
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        session = db_session.create_session()
        user = session.query(User).filter(User.login == login).first()
        if not user:
            message = 'Данного пользователя нет. Пожалуйста, пройдите регистрацию.'
        elif not user.check_password(form.password.data):
            message = 'Введён неверный пароль'
        else:
            login_user(user, remember=form.remember_me.data)
            resp = redirect('/main')
            session.close()
            return resp
    resp = render_template('login.html', title='Авторизация', form=form, message=message)
    return resp


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.login.data,
                    form.password.data)
        session = db_session.create_session()
        try:
            session.add(user)
            session.commit()
        except IntegrityError:
            return render_template('registration.html', title='Регистрация', form=form,
                                   message='Такой пользователь уже существует.')
        except Exception as e:
            print(e)
            return render_template('registration.html', title='Регистрация', form=form,
                                   message='Произошла ошибка. Пожалуйста, повторите попытку позже.')
        finally:
            session.close()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/')
@app.route('/main')
@login_required
def main_page():
    form = Main()
    session = db_session.create_session()
    session.add(current_user)
    session.merge(current_user)
    resp = render_template('main_page.html', title='Основная страница', form=form)
    session.close()
    return resp


@app.route('/profile/my_pets')
@login_required
def pets_page():
    session = db_session.create_session()
    pets = session.query(Pet).filter(Pet.user_id == current_user.id)
    session.close()
    return render_template("my_pets.html", pets=pets)


@app.route('/profile')
@login_required
def account_page():
    form = Profile()
    resp = render_template('profile.html', title='Основная страница', form=form)
    return resp


@app.route('/cats')
@login_required
def cats_page():
    form = Cats()
    resp = render_template('cats.html', title='Породы кошек', form=form)
    return resp


@app.route('/dogs')
@login_required
def dogs_page():
    form = Dogs()
    resp = render_template('dogs.html', title='Породы собак', form=form)
    return resp


@app.route('/birds')
@login_required
def birds_page():
    form = Birds()
    resp = render_template('birds.html', title='Породы птиц', form=form)
    return resp


@app.route('/profile/my_feedbacks')
@login_required
def fbcks_page():
    session = db_session.create_session()
    feedbacks = session.query(Feedback).filter(Feedback.user_id == current_user.id)
    session.close()
    return render_template("my_feedbacks.html", feedbacks=feedbacks)


@app.route('/profile/add_pet', methods=['GET', 'POST'])
@login_required
def add_pet():
    form = AddPet()
    if form.validate_on_submit():
        session = db_session.create_session()
        pet = Pet(pet_name=form.pet_name.data,
                  age=form.age.data,
                  type=form.type.data,
                  poroda=form.poroda.data)
        session.add(current_user)
        session.merge(current_user)
        current_user.pets.append(pet)
        session.commit()
        return redirect('/profile/my_pets')
    resp = render_template('add_my_pet.html', title='Добавить моего питомца', form=form)
    return resp


@app.route('/profile/add_feedback', methods=['GET', 'POST'])
@login_required
def add_feedback():
    form = AddFeedback()
    if form.validate_on_submit():
        feedback = Feedback(title=form.title.data,
                            content=form.content.data)
        session = db_session.create_session()

        current_user.news.append(feedback)
        session.merge(current_user)
        session.commit()
        return redirect('/my_feedbacks')
    resp = render_template('add_my_feedback.html', title='Добавить отзыв', form=form)
    return resp


@app.route('/cats/Персидская_кошка')
@login_required
def text():
    news_list = open("static/info/кошки/Персидская кошка/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Персидская_кошка.html', text=text)


@app.route('/cats/Регдолл')
@login_required
def text1():
    news_list = open("static/info/кошки/Рэгдолл/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Регдолл.html', text=text)


@app.route('/cats/Экзотическая_кошка')
@login_required
def text2():
    news_list = open("static/info/кошки/Экзотическая кошка/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Экзотическая_кошка.html', text=text)


@app.route('/cats/Русская_голубая')
@login_required
def text3():
    news_list = open("static/info/кошки/Русская голубая/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Русская_голубая.html', text=text)


@app.route('/cats/Мейн-кун')
@login_required
def text4():
    news_list = open("static/info/кошки/Мейн-кун/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Мейн_кун.html', text=text)


@app.route('/dogs/Бордер_колли')
@login_required
def text5():
    news_list = open("static/info/собаки/Бордер-колли/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Бордер_колли.html', text=text)


@app.route('/dogs/Доберман')
@login_required
def text6():
    news_list = open("static/info/собаки/Доберман/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Доберман.html', text=text)


@app.route('/dogs/Кане_корсо')
@login_required
def text7():
    news_list = open("static/info/собаки/Кане корсо/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Кане_корсо.html', text=text)


@app.route('/dogs/Немецкая_овчарка')
@login_required
def text8():
    news_list = open("static/info/собаки/Немецкая овчарка/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Немецкая_овчарка.html', text=text)


@app.route('/dogs/Хаски')
@login_required
def text9():
    news_list = open("static/info/собаки/Хаски/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Хаски.html', text=text)


@app.route('/birds/Волнистые_попугаи')
@login_required
def text10():
    news_list = open("static/info/птицы/Волнистые попугаи/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Волнистые_попугаи.html', text=text)


@app.route('/birds/Корелла')
@login_required
def text11():
    news_list = open("static/info/птицы/Корелла/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Корелла.html', text=text)


@app.route('/birds/Жако')
@login_required
def text12():
    news_list = open("static/info/птицы/Жако/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Жако.html', text=text)


@app.route('/birds/Какаду')
@login_required
def text13():
    news_list = open("static/info/птицы/Какаду/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Какаду.html', text=text)


@app.route('/birds/Сова')
@login_required
def text14():
    news_list = open("static/info/птицы/Сова/Текст.txt").readlines()
    text = ''.join(news_list)
    return render_template('Сова.html', text=text)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings_page():
    form = SettingsForm()
    session = db_session.create_session()
    if request.method == 'GET':
        form.login.data = current_user.login
    if form.validate_on_submit():
        if form.login.data:
            current_user.login = form.login.data
        if form.password.data:
            current_user.set_password(form.password.data)
        session.merge(current_user)
        session.commit()
        session.close()
        return redirect('/main')
    resp = render_template('settings.html', title='Настройки', form=form)
    session.close()
    return resp


@app.route('/all_feedbacks')
@login_required
def feedbacks():
    session = db_session.create_session()
    feedbacks = session.query(Feedback).all()
    return render_template("all_feedbacks.html", feedbacks=feedbacks)


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('user_id', required=True, type=int)


class ListResource(Resource):
    def get(self):
        session = db_session.create_session()
        feedbacks = session.query(Feedback).all()
        return jsonify({'news': [item.to_dict(
            only=('title', 'content', 'user.name')) for item in feedbacks]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        feedbacks = Feedback(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id']
        )
        session.add(feedbacks)
        session.commit()
        return jsonify({'success': 'OK'})


class Resource(Resource):
    def get(self, news_id):
        abort_if_feedbacks_not_found(id)
        session = db_session.create_session()
        feedbacks = session.query(Feedback).get(id)
        return jsonify({'feedbacks': feedbacks.to_dict(
            only=('title', 'content', 'user_id'))})

    def delete(self, news_id):
        abort_if_feedbacks_not_found(id)
        session = db_session.create_session()
        feedbacks = session.query(Feedback).get(id)
        session.delete(feedbacks)
        session.commit()
        return jsonify({'success': 'OK'})


if __name__ == '__main__':
    app.run()
