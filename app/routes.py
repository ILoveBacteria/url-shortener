from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm


@app.route('/')
def hello_world():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash(f'Username: {form.username.data} - Password: {form.password.data}')
        return redirect('/')

    return render_template('login.html', title='Login', form=form)

