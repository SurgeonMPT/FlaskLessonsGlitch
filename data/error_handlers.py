from flask import render_template


def not_found(e):
    return render_template("errors/404.html")


def forbidden(e):
    return render_template("errors/403.html")


def unauthorized(e):
    return render_template("errors/401.html")