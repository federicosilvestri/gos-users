from flask import render_template


def page_404(e):
    return render_template('404.html'), 404


def error_500(e):
    return render_template('500.html'), 500
