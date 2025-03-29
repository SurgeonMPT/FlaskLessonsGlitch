import flask
from flask import jsonify, make_response, render_template, request, redirect
from requests import get, post

from data import db_session
from data.models.news import New

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/news')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(New).all()
    news = [item.to_dict(only=('title', 'content', 'user.name')) for item in news]
    return jsonify({'news': news})


@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(New).get(news_id)
    if not news:
        # return render_template('errors/404.html', text="Такой новости нет!"), 404
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'news': news.to_dict(only=(
                'title', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/news_test_post', methods=['GET'])
def news_test_post():
    print(post('http://localhost:5000/api/news', json={}).json())

    print(post('http://localhost:5000/api/news',
               json={'title': 'Заголовок'}).json())

    print(post('http://localhost:5000/api/news',
               json={'title': 'Заголовок',
                     'content': 'Текст новости',
                     'user_id': 1,
                     'is_private': False}).json())
    return redirect("/")


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    news = New(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'id': news.id})


@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(New).get(news_id)
    if not news:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})
