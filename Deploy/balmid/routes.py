from flask import render_template, url_for, flash, redirect, request
from balmid import app, db, bcrypt
from balmid.forms import RegistrationForm, LoginForm, UpdateAccountForm, PorfolioForm
from balmid.models import User, Portfolio
from flask_login import login_user, current_user, logout_user, login_required
from balmid.custom_decorators import email_verifier
import datetime
import pytz
import phonenumbers
from random import randint
import secrets
import requests
import json


SECRET_KEY = "Bearer FLWSECK_TEST-b635125569aa7e8b749997814dbdca20-X"

def get_rave_ref():
    token = secrets.token_hex(10)
    taken_ref = session.query(Portfolio.rave_ref)
    while token in taken_ref:
        token = secrets.token_hex(10)
    return token


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", title='Home')

@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Welcome, {current_user.first_name}", 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:    
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("loginn.html", title='Log In', form=form)

@app.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, 
                    email=form.email.data, phone=form.phone.data,
                    password=hashed_password, date_created=datetime.datetime.now(tz=pytz.timezone('Africa/Lagos')) )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!, You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/products')
def products():
    return render_template("products.html", title="Products")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/personalinvestment')
def personalinvestment():
    return render_template("personalinvestment.html")

@app.route('/dashboard')
@login_required
#@email_verifier
def dashboard():
    try:
        test_completed = Portfolio.query.filter_by(user_id=current_user.id, rave_status = 'Active', completed=False, paid_in=True)
        for x in test_completed.payout_date:
            if datetime.datetime.now(tz=pytz.timezone('Africa/Lagos')) >= x:
                test_completed.completed = True
        db.session.commit()
    except:
        pass
    active_ports = Portfolio.query.filter_by(user_id=current_user.id, rave_status = 'Active', show=True, completed=False)
    pending_ports = Portfolio.query.filter_by(user_id=current_user.id, rave_status = 'Pending', show=True)
    failed_ports = Portfolio.query.filter_by(user_id=current_user.id, rave_status = 'Failed', show=True)
    return render_template("dashboard.html", title="Dashboard", active_ports=active_ports, pending_ports=pending_ports, failed_ports=failed_ports,
                            local_number = ((phonenumbers.format_number(phonenumbers.parse(current_user.phone, None), 
                            phonenumbers.PhoneNumberFormat.NATIONAL)).replace(' ','')))

@app.route('/profile', methods=["POST", "GET"])
@login_required
#@email_verifier
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    return render_template("profile.html", form=form, title="Profile")


@app.route('/portfolio', methods=["POST", "GET"])
@login_required
#@email_verifier
def portfolio():
    form = PorfolioForm()
    if form.validate_on_submit():
        port = Portfolio(product_name=form.product_name.data, product_code=form.product_code.data, units=int(form.units.data), 
                        amount_paid =int(form.units.data * form.amount_per_unit.data), date_created= datetime.datetime.now(tz=pytz.timezone('Africa/Lagos')) , 
                        interest_rate=int(form.interest_rate.data), duration= int(form.duration.data), 
                        payout_amount= int((form.units.data * form.amount_per_unit.data) * (1 + (form.interest_rate.data/100))), 
                        payout_date= (datetime.datetime.now(tz=pytz.timezone('Africa/Lagos')) + datetime.timedelta(days=form.duration.data)), 
                        rave_ref=secrets.token_hex(6), author=current_user )
        db.session.add(port)
        db.session.commit()
        flash('Portfolio Created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('portfolio.html', form=form, title="Portfolio")


@app.route("/json", methods=["POST"])
def json_example():
    if request.is_json:
        req_data = request.get_json()
        tran_ref = req_data['body']['data']['tx_ref']
        tran_status = req_data['body']['data']['status']
        tran_curr = req_data['body']['data']['currency']
        tran_amount = req_data['body']['data']['amount']

        port = Portfolio.query.filter_by(rave_ref=tran_ref).first()
        verified_currency = (tran_curr == 'NGN')
        verified_amount = (tran_amount >= port.amount_paid)
        if port and verified_currency and verified_amount:
            
            if  tran_status == 'successful':
                if port.rave_status != 'Active':
                    port.rave_status = 'Active'
                    port.paid_in = True
                    port.date_paid = datetime.datetime.now(tz=pytz.timezone('Africa/Lagos'))
                    port.payout_date = (datetime.datetime.now(tz=pytz.timezone('Africa/Lagos')) + datetime.timedelta(days=int(port.duration)))
                    db.session.commit()
        
                    return "S", 200
        else:   
            port.rave_status = 'Failed'
            db.session.commit()
            return "F", 200

    return "Request wasn't JSON", 400


@app.route('/payment_history')
@login_required
#@email_verifier
def paymenthistory():
    purchases = Portfolio.query.filter_by(user_id=current_user.id, paid_in = True)
    returns = Portfolio.query.filter_by(user_id=current_user.id, completed = True)

    return render_template("paymenthistory.html", title="Payment History", purchases=purchases, returns=returns)


@app.route('/verify_payment/<txRef>')
@login_required
def verify(txRef):
    url = 'https://api.flutterwave.com/v3/transactions' + '?tx_ref=' + txRef
    headers = {
        'Content-Type': 'application/json',
        "Authorization": SECRET_KEY,
        "Connection": "keep-alive"}
    response = requests.get(url, headers=headers)
    res = json.loads(response.text)
    return res
    tran_amount = response['data']
    for tran_amoun in tran_amount:
        print(tran_amoun)
    return tran_amoun
    # tran_status = response['data']['status']
    # tran_curr = response['data']['currency']
    # tran_amount = response['data']['amount']
    # return (tran_ref, tran_status, tran_curr, tran_amount)

@app.route('/delete_portfolio/<txRef>', methods=['GET','POST'])
@login_required
def delete_portfolio(txRef):
    port = Portfolio.query.filter_by(rave_ref=txRef).first()
    return render_template("deleteportfolio.html", title="Delete Portfolio", port=port)

@app.route('/confirm_delete/<txRef>', methods=['POST'])
@login_required
def confirm_delete(txRef):
    port = Portfolio.query.filter_by(rave_ref=txRef).first()
    if port.author != current_user:
        abort(403)
    port.show = False
    db.session.commit()
    flash('Portfolio deleted!', 'success')
    return redirect(url_for('dashboard'))
