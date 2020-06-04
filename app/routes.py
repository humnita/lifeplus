from flask import render_template, flash, redirect, url_for, request
from app import app, db 
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User 
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required # protects views against anonymous users
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # takes the password has stored with the user and determine if
        #  password entered matches the hash 
        #  if either username is invalid or password is incorrect, do
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        # if both username and password and correct 
        #   CONDITIONS  :
        #       1. URL does not have a next argument:
        #           - redirected to index page
        #       2. URL includes a next argument set to a relative path:
        #           - redirected to that URL
        #       3. URL includes a next argument that includes a domain name::
        #           - redirected to index page to ensure security from 
        #               malicious sites 

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)