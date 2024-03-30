from PIL import Image
import secrets
import os
import requests
from flask_mail import Message as MG
from app import db, mail
from app.main import bp
from flask import render_template, flash, redirect, url_for, request, current_app
from app.main.forms import (EditProfileForm, 
                       PlaceOrderForm, FilterSellersForm, CheckOrderForm, DeleteOrdersForm, MessageForm)
from flask_login import current_user, login_required
from app.models import Users, Order, Message


@bp.route('/')
@bp.route('/index')
def index():
    """entry page of wesite"""
    return render_template('index.html')


@bp.route('/home')
@login_required
def home():
    """redirects a user to thier specific home page e.g buyer to /buyer and seller to /seller"""
    if current_user.is_authenticated:
        """orders = Order.query.filter_by(purchaser=current_user).all()
        key = '994ee93c240c488cafd112500240103'
        location = current_user.county
        url = "http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no".format(key, location)
        resp = requests.get(url).json()
        user = Users.query.filter_by(email=current_user.email).first()"""
        if current_user.email == current_app.config['ADMIN_EMAIL']:
            return redirect(url_for('main.admin'))
        elif current_user.type == 'buyer':
            # return render_template('buyers.html', title='Home Page', user=user, resp=resp, orders=orders)
            return redirect(url_for('main.buyer'))
        elif current_user.type == 'seller':
            return redirect(url_for('main.seller'))
            # return render_template('sellers.html', title='Home Page', user=user, resp=resp)
    return render_template('index.html')


@bp.route('/buyer', methods=['GET', 'POST'])
@login_required
def buyer():
    """buyer section in website"""
    if current_user.is_authenticated:
        orders = Order.query.filter_by(purchaser=current_user).order_by(Order.id.desc()).limit(5).all()
        key = '994ee93c240c488cafd112500240103'
        location = current_user.county
        url = 'http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no'.format(key, location)
        resp = requests.get(url).json()
        user = Users.query.filter_by(email=current_user.email).first()
    form = FilterSellersForm()
    if form.validate_on_submit():
        return redirect(url_for('main.place_order', county=form.county.data))
    return render_template('buyers.html', title='Home Page', user=user, resp=resp, orders=orders, form=form)


@bp.route('/seller', methods=['GET', 'POST'])
@login_required
def seller():
    """seller/vender section in website"""
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


@bp.route('/order_history')
@login_required
def order_history():
    """if a seller/vendor wants to see all of their order in detail"""
    orders = Order.query.filter_by(seller=current_user).all()
    return render_template('order_history.html', orders=orders)


@bp.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """if user wants to see their profile section"""
    if current_user.is_authenticated:
        image = url_for("static", filename='pictures/' + current_user.profile_pic)
        user = Users.query.filter_by(email=current_user.email).first()
        return render_template('profile.html',user=user, title='Profile Page', image=image)


def delete_pic():
    """deletes an image"""
    if current_user.profile_pic != 'default.jpg':
        old_pic = os.path.join(current_app.root_path + "/static/pictures/" + current_user.profile_pic)
        os.remove(old_pic)


def save_image(pic_data):
    """saves uploaded image and deletes previous image if any"""
    _, fn_ext = os.path.splitext(pic_data.filename)
    random_hex = secrets.token_hex(8)
    filename = random_hex + fn_ext
    picture_path = os.path.join(current_app.root_path, "static/pictures", filename)
    image_size = (125, 125)
    i = Image.open(pic_data)
    i.thumbnail(image_size)
    i.save(picture_path)
    # the commented line below saves picture-as-is while 4 lines above create a thumbnail 125 by 125 pixels size
    """pic_data.save(picture_path)"""

    delete_pic()
    return filename


@bp.route('/edit/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """incase a user wants to modify their details in their profile"""
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            img_name = save_image(form.profile_pic.data)
            current_user.profile_pic = img_name
        current_user.county = form.county.data
        current_user.username = form.username.data
        current_user.phone_number =form.phone_number.data
        db.session.commit()
        flash("Successfully updated profile")
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.county.data = current_user.county
        form.username.data = current_user.username
        form.phone_number.data = current_user.phone_number
    return render_template('edit_profile.html', title='Profile Edit', form=form)


@bp.route('/order/<county>', methods=['GET', 'POST'])
@login_required
def place_order(county):
    """if user wants to place an order, has functionality to filter users given a county"""
    if county == 'all':
        sellers = Users.query.filter_by(type="seller").all()
    else:
        sellers = Users.query.filter_by(type="seller").filter_by(county=county).all()
    """if len(sellers) == 0:
        sellers = Users.query.filter_by(type=2).all()"""
    form = PlaceOrderForm()
    if form.validate_on_submit():
        purchaser = current_user
        seller = Users.query.filter_by(id=int(form.id.data)).filter_by(type="seller").first_or_404()
        order = Order(purchaser=purchaser, seller=seller)
        db.session.add(order)
        db.session.commit()
        flash("Order placed successfully")

        msg = MG("New Order", sender=current_app.config["MAIL_USERNAME"], recipients=[seller.email])
        msg.body = """You have received a new order. Kindly log in to check it out.'\n\nSincerely,\nMaji App"""
        mail.send(msg)

        return redirect(url_for("main.home"))
    return render_template('place_order.html', form=form, sellers=sellers)


@bp.route('/delete_me')
@login_required
def delete_me():
    """incase a user wants to delete their account in profile page section"""
    if current_user.email != current_app.config['ADMIN_EMAIL']:
        delete_pic()
        db.session.delete(current_user)
        db.session.commit()
        flash("Account successfully deleted")
        return redirect(url_for("main.index"))
    flash('Admin not deletable')
    return redirect(url_for('main.profile'))


@bp.route('/me/orders')
@login_required
def my_orders():
    """incase purchaser wants to see a detailed view of all of their placed orders and their statuses"""
    orders = Order.query.filter_by(purchaser=current_user).all()
    return render_template('my_orders.html', orders=orders)


@bp.route('/admin')
@login_required
def admin():
    """handles admin view of web site"""
    if current_user.email == current_app.config['ADMIN_EMAIL']:
        orders = Order.query.all()
        users = Users.query.all()
        # users.pop(0)
        return render_template('admin.html', orders=orders, users=users)


@bp.route('/admin/orders/<id>', methods=["GET", "POST"])
@login_required
def delete_orders(id):
    """delete an order given ID or all orders"""
    if current_user.email == current_app.config['ADMIN_EMAIL']:
        form = DeleteOrdersForm()
        orders = Order.query.all()
        if form.validate_on_submit():
            for order in orders:
                if order.id == int(form.id.data):
                    db.session.delete(order)
                    db.session.commit()
                    flash("Order deleted")
            return redirect(url_for('main.admin'))
        if id == 'all':
            for order in orders:
                db.session.delete(order)
            db.session.commit()
            flash("All orders successfully deleted")
            return redirect(url_for("main.admin"))
        return render_template('delete_orders.html', form=form, orders=orders)
    return redirect('main.home')

@bp.route('/admin/users/<id>', methods=['GET', 'POST'])
@login_required
def delete_users(id):
    """delete a user given ID or all users except admin user"""
    if current_user.email == current_app.config['ADMIN_EMAIL']:
        form = DeleteOrdersForm()
        users = Users.query.all()
        if form.validate_on_submit():
            for user in users:
                if user.id == int(form.id.data) and user != current_user:
                    db.session.delete(user)
                    db.session.commit()
                    flash("User deleted")
                if user.id == int(form.id.data) and user == current_user:
                    flash("Admin not deletable")
            return redirect(url_for('main.admin'))
        if id == 'all':
            users.pop(0)
            for user in users:
                db.session.delete(user)
            db.session.commit()
            flash("All users successfully deleted")
            return redirect(url_for("main.admin"))
        return render_template('delete_users.html', form=form, users=users)
    return redirect(url_for('main.home'))


@bp.route('/new_message', methods=["GET", "POST"])
@login_required
def new_message():
    form = MessageForm()
    if form.validate_on_submit():
        receiver = Users.query.filter_by(email=form.to.data).first_or_404()
        message = Message(content=form.content.data, sender=current_user, receiver=receiver)
        db.session.add(message)
        db.session.commit()
        flash("message sent")
        return redirect(url_for("main.inbox"))
    return render_template("new_message.html", form=form, title="New Message")

@bp.route('/inbox', methods=["GET", "POST"])
@login_required
def inbox():
    """messages = Message.query.filter_by(receiver=current_user).all()"""
    page = request.args.get("page", 1, type=int)
    messages = Message.query.filter_by(receiver=current_user).order_by(Message.id.desc()).paginate(page=page,per_page= current_app.config['PER_PAGE'], error_out=False)
    next_url = url_for("main.inbox", page=messages.next_num) if messages.has_next else None
    prev_url = url_for("main.inbox", page=messages.prev_num) if messages.has_prev else None
    return render_template('inbox.html', messages=messages, title="MyInbox", next_url=next_url, prev_url=prev_url)


@bp.route('/delete/messagei/<id>')
@login_required
def delete_message(id):
    messages = Message.query.filter_by(receiver=current_user).all()
    if id == "all":
        for message in messages:
            db.session.delete(message)
        db.session.commit()
        flash("You inbox has been deleted successfully")
        return redirect(url_for('main.inbox'))
