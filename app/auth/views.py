from flask import render_template, request, redirect, url_for
from login import login_user, logout_user
from app.auth import auth
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        username = form.get('username')
        password = form.get('password')
        print(username)
        user = User.query.filter_by(username=username).first()
        if user is None:
            error = 'None exixstant Username'
            return render_template('login.html', error=error)
        is_correct_password = user.check_password(password)
        print(is_correct_password)
        if not is_correct_password:
            error = 'Non existant Password'
            return render_template('login.html', error=error)
        login_user(user)
        return redirect('/')
    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = request.form
        username = form.get("username")
        email = form.get("email")
        password = form.get("password")
        confirm_password = form.get("confirm_password")
        if username is None or password is None or email is None or confirm_password is None:
            error = 'Input required'
            return render_template('signup.html', error=error)
        if ' ' in username:
            error = 'Username should be one word'
            return render_template('signup.html', error=error)
        if password != confirm_password:
            error = "Invalid Password"
            return render_template('signup.html', error=error)
        else:
            user = User.query.filter_by(username=username).first()
            if user is not None:
                error = 'Name already exists'
                return render_template('signup.html', error=error)
            user = User.query.filter_by(email=email).first()
            if user is not None:
                error = ' Email already exists'
                return render_template('signup.html', error=error)
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

            # email_message("HELLO!Welcome to  Pitch", "email/hello", user.email, user=user)
            return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
