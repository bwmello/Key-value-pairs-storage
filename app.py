# Flask
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user, login_user, logout_user

# Custom
from . import app, db
from models import KeyValuePair, User
from forms import KeyValuePairForm, LoginForm, RegistrationForm


# Homepage and non auth related user actions (creating and modifying user's KeyValuePairs)
# TODO Provide delete KeyValuePair button and functionality
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = KeyValuePairForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_kvp = KeyValuePair.query.filter_by(key=form.key.data).one_or_none()
            if existing_kvp:
                if existing_kvp.user_id == current_user.id:
                    existing_kvp.value = form.value.data
                    db.session.commit()
                else:
                    flash('Key %s already taken. Please try another' % (form.key.data))
            else:
                new_kvp = KeyValuePair(key=form.key.data, value=form.value.data, user_id=current_user.id)
                db.session.add(new_kvp)
                db.session.commit()
    kvps = KeyValuePair.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', kvps=kvps, form=form)


# Generic API calls for getting KeyValuePairs and setting userless KeyValuePairs
# TODO Add authentication, either an APIKey or User credentials
@app.route('/api/kvp/get/<key>', methods=['GET'])
def get_kvp(key):
    kvp = KeyValuePair.query.filter_by(key=str(key)).one_or_none()
    return kvp.value, 201


@app.route('/api/kvp/set', methods=['POST'])
def set_kvp():
    if not request.json or 'key' not in request.json.keys():
        return "Missing or malformed json arguments", 400
    set_kvp = None
    existing_kvp = KeyValuePair.query.filter_by(key=str(request.json['key'])).one_or_none()
    if existing_kvp:
        existing_kvp.value = request.json.get('value', None)
        set_kvp = existing_kvp
    else:
        set_kvp = KeyValuePair(key=request.json['key'], value=request.json.get('value', None))
        db.session.add(set_kvp)
    db.session.commit()
    return "Successfully set %s: %s" % (set_kvp.key, set_kvp.value), 201


# All user authentication related calls and pages
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)  # Could pass remember=True, but no interest in persistence after session expiration
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


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
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)
