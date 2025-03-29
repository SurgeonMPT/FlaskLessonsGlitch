from flask import Blueprint, render_template, redirect, abort, request
from flask_login import login_required, current_user

from data import db_session
from data.models.news import New
from forms.news import NewsForm

bp = Blueprint('news', __name__, url_prefix='/news')

@bp.route('/')
@login_required
def news_list():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(New).filter(
            (New.user == current_user) | (New.is_private != True))
    else:
        news = db_sess.query(New).filter(New.is_private != True)
    return render_template("index.html", news=news)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = New()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news/add_news.html',
                          title='Добавление новости',
                          form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(New).filter(New.id == id,
                                        New.user == current_user
                                        ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(New).filter(New.id == id,
                                        New.user == current_user
                                        ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news/add_news.html',
                          title='Редактирование новости',
                          form=form)

@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(New).filter(New.id == id,
                                    New.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')