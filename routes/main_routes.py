from flask import Blueprint, render_template, redirect, request, make_response, session, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.models.users import User
from data.models.news import New
from forms.user import LoginForm, RegisterForm

bp = Blueprint('main', __name__)

@bp.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                      max_age=60*60*24*365*2)
    else:
        res = make_response("Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                      max_age=60*60*24*365*2)
    return res

@bp.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session.permanent = True
    session['visits_count'] = visits_count + 1
    return make_response(f"Вы пришли на эту страницу {visits_count + 1} раз")

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@bp.route("/")
@bp.route("/index")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(New).filter(
            (New.user == current_user) | (New.is_private != True))
    else:
        news = db_sess.query(New).filter(New.is_private != True)
    return render_template("index.html", news=news)