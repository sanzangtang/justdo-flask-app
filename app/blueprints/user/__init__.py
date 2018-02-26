from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from app.blueprints.user.forms import LoginForm, RegisterForm
from app.blueprints.user.models import User
from app import db

bp_user = Blueprint('bp_user', __name__)


@bp_user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('bp_dashboard.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_username(username=form.username.data)

        if user is None:
            flash('User does not exist.', 'alert alert-danger')
            return redirect(url_for('bp_user.login'))

        # may raise problem if database does not handle binary well
        if user.verify_password(form.password.data):
            login_user(user)
            flash('Welcome, {}!'.format(user.username), 'alert alert-success')
            # safe url check?
            return redirect(url_for('bp_dashboard.dashboard'))
        else:
            flash('Wrong password, please try agin.',
                  'alert alert-danger')
            return redirect(url_for('bp_user.login'))

    return render_template('login.html', form=form)


@bp_user.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have logged out.', 'alert alert-info')
    return redirect(url_for('bp_index.index'))


@bp_user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        if User.find_by_username(username):
            flash("The username has been taken.",
                  "alert alert-danger")
            return redirect(url_for('bp_user.register'))
        else:
            user = User(username=username)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Welcome {}, you're now ready to go.".format(username),
                  "alert alert-success")
            # add auto login after register
            return redirect(url_for('bp_user.login'))
    return render_template('register.html', form=form)
