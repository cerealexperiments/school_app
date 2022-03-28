import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from schoolapp import app, db, bcrypt
from schoolapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, InsertForm
from schoolapp.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    users = User.query.all()
    return render_template('home.html', users=users)


@app.route('/index')
def index():
    users = User.query.all()
    return render_template("index.html", users=users)


@app.route('/insert', methods=['POST'])
def insert():
    form = InsertForm()
    if form.validate_on_submit():
        user = User(full_name=form.full_name.data, email=form.email.data, password=hashed_password,
                    date_of_birth=form.date_of_birth.data, address=form.address.data, grade=form.grade.data,
                    phone_number=form.phone_number.data, additional_info=form.additional_info.data,
                    tuition_fee=form.tuition_fee.data, gender=form.gender.data)
        db.session.add(user)
        db.session.commit()
        flash("Student Inserted Successfully")
        return redirect(url_for('index.html'))
    return render_template('index.html', title='index', form=form)



@app.route('/update', methods=['GET', 'POST'])
def update():
    form = InsertForm()
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.date_of_birth = form.date_of_birth.data
        current_user.grade = form.grade.data
        current_user.address = form.address.data
        current_user.gender = form.gender.data
        current_user.active = form.active.data
        current_user.tuition_fee = form.tuition_fee.data
        current_user.additional_info = form.additional_info.data
        db.session.commit()
        flash("Student Updated Successfully")
        return redirect(url_for('index'))
    else:
        return redirect(url_for("index"))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash("Student Deleted Successfully")

    return redirect(url_for('index'))



@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(full_name=form.full_name.data, email=form.email.data, password=hashed_password,
                    date_of_birth=form.date_of_birth.data, address=form.address.data, grade=form.grade.data,
                    phone_number=form.phone_number.data, additional_info=form.additional_info.data,
                    tuition_fee=form.tuition_fee.data, gender=form.gender.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.date_of_birth = form.date_of_birth.data
        current_user.grade = form.grade.data
        current_user.address = form.address.data
        current_user.additional_info = form.additional_info.data
        current_user.tuition_fee = form.tuition_fee.data
        current_user.phone_number = form.phone_number.data
        current_user.gender = form.gender.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
        form.date_of_birth.data = current_user.date_of_birth
        form.grade.data = current_user.grade
        form.address.data = current_user.address
        form.additional_info.data = current_user.additional_info
        form.gender.data = current_user.gender
        form.tuition_fee.data = current_user.tuition_fee
        form.phone_number.data = current_user.phone_number
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

