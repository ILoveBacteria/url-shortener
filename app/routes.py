import random
import string

from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import LoginForm, SignUpForm, NewLinkForm
from app.models import User, Link, Visit

from sqlalchemy import func


def random_slug(size=6, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/')
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
            flash('Username or password is incorrect', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        flash('Login successfully', 'success')
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
        flash('Sign up successfully', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/links/new', methods=['GET', 'POST'])
@login_required
def create_new_link():
    form = NewLinkForm()

    if form.validate_on_submit():
        slug = random_slug()
        while Link.query.filter_by(slug=slug).first() is not None:
            slug = random_slug()

        link = Link(slug=slug, redirect_url=form.redirect_url.data, user=current_user)
        db.session.add(link)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('new_link.html', title='Create New Link', form=form)


@app.route('/r/<slug>')
def short_url(slug):
    link = Link.query.filter_by(slug=slug).first()
    if link is None:
        return '404', 404

    visit = Visit(ip=request.remote_addr, referer=request.referrer, user_agent=request.user_agent.string, link=link)
    db.session.add(visit)
    db.session.commit()
    return redirect(link.redirect_url)


@app.route('/links')
@login_required
def links():
    current_page = request.args.get('page', 1, type=int)
    links = db.session.query(
        Link.id,
        Link.redirect_url,
        Link.slug,
        Link.user_id,
        func.count(Visit.id)
    )\
        .filter_by(user_id=current_user.id)\
        .join(Visit, isouter=True)\
        .group_by(Link.id)\
        .order_by(Link.id.desc())\
        .paginate(current_page, 4)

    return render_template('links.html', links=links, title='My Links')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'icon/favicon.ico')


@app.route('/android-chrome-192x192.png')
def android_chrome_192():
    return send_from_directory('static', 'icon/android-chrome-192x192.png')


@app.route('/android-chrome-512x512.png')
def android_chrome_512():
    return send_from_directory('static', 'icon/android-chrome-512x512.png')
