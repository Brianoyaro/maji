import smtplib
from flask_mail import Message as MG
from app import  db, mail
from app.auth import bp
from app.auth.auth_forms import LoginForm, RegistrationForm, ResetRequestForm, ActualRequestForm
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, Message


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """login a user in the website"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Successfully logged in')
        if user.email == 'admin@admin.com':
            return redirect(url_for("main.admin"))        
        """incase app redirected to /login because of @login_required"""
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('main.home')
        return redirect(next_page) 
    return render_template("auth/login.html", title="Login", form=form)


@bp.route('/logout')
@login_required
def logout():
    """logout of application"""
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registering new users"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data, county=form.county.data, type=form.type.data, phone_number=form.phone_number.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registeration completed")
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', form=form, title='Registration Page')


def reset_email(user):
    token = user.get_token()
    msg = MG(subject="Password Reset", sender=current_app.config["MAIL_USERNAME"], recipients=[user.email])
    msg.body = render_template("email/msg.txt", user=user, token=token)
    msg.html = render_template("email/msg.html", user=user, token=token)
    mail.send(msg)
    """with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])

        subject = "Password Reset"
        body = render_template("email/msg.html", user=user, token=token)

        msg = "Subject: {}\n\n{}".format(subject, body)
        smtp.sendmail(current_app.config['MAIL_USERNAME'], user.email, msg)"""


@bp.route('/reset_request', methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            reset_email(user)
        flash("Check you email for instructions")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_request.html", title="Password Reset", form=form)


@bp.route('/password_reset/<token>', methods=["GET", "POST"])
def actual_password_reset(token):
    user = Users.check_token(token)
    if user is None:
        flash("Invalid/expired token")
        return redirect(url_for("auth.login"))
    form = ActualRequestForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Password updated")
        return redirect(url_for("auth.login"))
    return render_template("auth/actual_password_reset.html", form=form, title="Password Reset")
