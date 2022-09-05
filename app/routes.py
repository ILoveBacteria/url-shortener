import random
import string

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import LoginForm, SignUpForm, NewLinkForm
from app.models import User, Link


def random_slug(size=6, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Username or password is incorrect')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        flash('Login successfully')
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)  # type: ignore
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sign up successfully')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/links/new', methods=['GET', 'POST'])
@login_required
def create_new_link():
    form = NewLinkForm()

    if form.validate_on_submit():
        link = Link(slug=random_slug(), redirect_url=form.redirect_url.data, user=current_user)
        db.session.add(link)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('new_link.html', title='Create New Link', form=form)


@app.route('/r/<slug>')
def short_url(slug):
    link = Link.query.filter_by(slug=slug).first()
    if link is not None:
        return redirect(link.redirect_url)
    return '404', 404
