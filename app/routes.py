import requests
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PlaceOrderForm, FilterSellersForm, CheckOrderForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, Order


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html') # customize index to handle nuyers and sellers by making it uniues to each I suppose by current_user.type == 1 then buyers else seller


@app.route('/home')
@login_required
def home():
    if current_user.is_authenticated:
        """orders = Order.query.filter_by(purchaser=current_user).all()
        key = '994ee93c240c488cafd112500240103'
        location = current_user.county
        url = "http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no".format(key, location)
        resp = requests.get(url).json()
        user = Users.query.filter_by(email=current_user.email).first()"""
        if current_user.type == '1':
            # return render_template('buyers.html', title='Home Page', user=user, resp=resp, orders=orders)
            return redirect(url_for('buyer'))
        else:
            return redirect(url_for('seller'))
            # return render_template('sellers.html', title='Home Page', user=user, resp=resp)


@app.route('/buyer', methods=['GET', 'POST'])
@login_required
def buyer():
    if current_user.is_authenticated:
        orders = Order.query.filter_by(purchaser=current_user).all()
        key = '994ee93c240c488cafd112500240103'
        location = current_user.county
        url = "http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no".format(key, location)
        resp = requests.get(url).json()
        user = Users.query.filter_by(email=current_user.email).first()
    form = FilterSellersForm()
    if form.validate_on_submit():
        return redirect(url_for('place_order', county=form.county.data))
    return render_template('buyers.html', title='Home Page', user=user, resp=resp, orders=orders, form=form)


@app.route('/seller', methods=['GET', 'POST'])
@login_required
def seller():
    if current_user.is_authenticated:
        orders = Order.query.filter_by(seller=current_user).filter_by(checked=False).all()
        key = '994ee93c240c488cafd112500240103'
        location = current_user.county
        url = "http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no".format(key, location)
        resp = requests.get(url).json()
        user = Users.query.filter_by(email=current_user.email).first()
    form = CheckOrderForm()
    if form.validate_on_submit():
        order = Order.query.filter_by(id=form.id.data).first()
        order.checked = True
        db.session.add(order)
        db.session.commit()
        flash("You have marked the order as completed")
    return render_template('sellers.html', title='Home Page', user=user, resp=resp, orders=orders, form=form)

@app.route('/order_history')
@login_required
def order_history():
    orders = Order.query.filter_by(seller=current_user).all()
    return render_template('order_history.html', orders=orders)
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
        flash("Registeration completed")
        return redirect(url_for('login'))
    return render_template('registration.html', form=form, title='Registration Page')


@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.is_authenticated:
        user = Users.query.filter_by(email=current_user.email).first()
        return render_template('profile.html',user=user, title='Profile Page')


@app.route('/edit/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.county = form.county.data
        current_user.username = form.username.data
        current_user.phone_number =form.phone_number.data
        db.session.commit()
        flash("Successfully updated profile")
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.county.data = current_user.county
        form.username.data = current_user.username
        form.phone_number.data = current_user.phone_number
    return render_template('edit_profile.html', title='Profile Edit', form=form)


@app.route('/order/<county>', methods=['GET', 'POST'])
@login_required
def place_order(county):
    if county == 'all':
        sellers = Users.query.filter_by(type=2).all()
    else:
        sellers = Users.query.filter_by(type=2).filter_by(county=county).all()
    """if len(sellers) == 0:
        sellers = Users.query.filter_by(type=2).all()"""
    form = PlaceOrderForm()
    if form.validate_on_submit():
        purchaser = current_user
        seller = Users.query.filter_by(id=int(form.id.data)).filter_by(type=2).first_or_404()
        order = Order(purchaser=purchaser, seller=seller)
        db.session.add(order)
        db.session.commit()
        flash("Order placed successfully")
        return redirect(url_for("home"))
    return render_template('place_order.html', form=form, sellers=sellers)


@app.route('/delete_me')
@login_required
def delete_me():
    """
    if current_user.is_authenticated:
        users = Users.query.all()
        for user in users:
            if user == current_user:
                db.session.delete(user)
                db.session.commit()
                flash("Account Deleted Successfully")
                return redirect(url_for("index"))"""
    db.session.delete(current_user)
    db.session.commit()
    flash("Account successfully deleted")
    return redirect(url_for("index"))
