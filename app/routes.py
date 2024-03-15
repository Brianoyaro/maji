from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html') # customize index to handle nuyers and sellers by making it uniues to each I suppose by current_user.type == 1 then buyers else seller


@app.route('/home')
@login_required
def home():
    if current_user.is_authenticated:
        if current_user.type == '1':
            return render_template('buyers.html', title='Home Page')
        else:
            return render_template('sellers.html', title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Successfully logged in')
        """incase app redirected to /login because of @login_required"""
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('home')
        return redirect(next_page) 
    return render_template("login.html", title="Login", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data, county=form.county.data, type=form.type.data, phone_number=form.phone_number.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form, title='Registration Page')
