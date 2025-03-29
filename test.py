from data.models.news import New
from data.models.posts import Post
from data.models.users import User


def default_test(db_session):
    db_sess = db_session.create_session()

    if not db_sess.query(Post).filter(Post.name == "Администратор").first():
        post = Post()
        post.name = "Администратор"
        db_sess.add(post)

    if not db_sess.query(Post).filter(Post.name == "Модератор").first():
        post = Post()
        post.name = "Модератор"
        db_sess.add(post)

    if not db_sess.query(Post).filter(Post.name == "Пользователь").first():
        post = Post()
        post.name = "Пользователь"
        db_sess.add(post)
    db_sess.commit()

    if not db_sess.query(User).filter(User.email == "email@email.ru").first():
        user = User()
        user.name = "Пользователь 1"
        user.about = "биография пользователя 1"
        user.email = "email@email.ru"
        db_sess.add(user)
    db_sess.commit()

    user = db_sess.query(User).filter(User.email == "email@email.ru").first()
    user.post_id = 3
    db_sess.commit()

    if not db_sess.query(New).filter(New.title == "Первая новость").first():
        news = New(title="Первая новость", content="Привет блог!",
                   user_id=1, is_private=False)
        db_sess.add(news)

    if not db_sess.query(New).filter(New.title == "Вторая новость").first():
        user = db_sess.query(User).filter(User.id == 1).first()
        news = New(title="Вторая новость", content="Уже вторая запись!",
                   user=user, is_private=False)
        db_sess.add(news)

    if not db_sess.query(New).filter(New.title == "Личная запись").first():
        user = db_sess.query(User).filter(User.id == 1).first()
        news = New(title="Личная запись", content="Эта запись личная",
                   is_private=True)
        user.news.append(news)
    db_sess.commit()