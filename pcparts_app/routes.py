from flask import Blueprint, render_template, request, url_for, redirect, flash
from . import db, bcrypt  # Import from the __init__.py file
from .models import User
from .forms import RegistrationForm, LoginForm
from .scraper import get_all_products
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/login", methods = ['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Database query to find by email
        user = User.query.filter_by(email=form.email.data).first()

        # Checking if the user exists AND the password is correct
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            # Log user in
            login_user(user, remember=form.remember.data)
            flash('Login Successful', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
       
        # Create a new user instance
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user) # Adding to database
        db.session.commit()
        flash('Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', title = 'Register', form = form)

@main.route("/findparts", methods=['GET', 'POST'])
def new_parts():
    products = []
    query = ""

    # Only runs when the user submits the form
    if request.method == 'POST':
        query = request.form.get('user_text', '')
        is_used = 'used_parts_check' in request.form
        if query:
            # Returns a list of products
            products = get_all_products(query, is_used)
        
    return render_template("FindParts.html", products = products, query=query)