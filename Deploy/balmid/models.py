from balmid import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean(), default=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    extra_str = db.Column(db.String(50), nullable=True)
    extra_int = db.Column(db.Integer, nullable=True)
    extra_bool = db.Column(db.Boolean(), nullable=True)

    portfolio = db.relationship('Portfolio', backref='author', lazy=True)

    
    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), nullable=False)
    product_code = db.Column(db.String(20), nullable=False)
    units = db.Column(db.Integer, nullable=False, default=1)
    amount_paid = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    interest_rate = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.String(10), nullable=False)
    payout_amount = db.Column(db.Integer, nullable=False)
    payout_date = db.Column(db.DateTime, nullable=False)
    date_paid = db.Column(db.DateTime, nullable=True)
    rave_ref = db.Column(db.String(14), nullable=False)
    rave_status = db.Column(db.String(20), nullable=False, default='Pending')
    show = db.Column(db.Boolean(), nullable=False, default=True)
    completed = db.Column(db.Boolean(), nullable=False, default=False)
    paid_in  = db.Column(db.Boolean(), nullable=False, default=False) 
    paid_out  = db.Column(db.Boolean(), nullable=False, default=False)

    extra_str = db.Column(db.String(50), nullable=True)
    extra_int = db.Column(db.Integer, nullable=True)
    extra_bool = db.Column(db.Boolean(), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"User('Product name: {self.product_name}', 'Product Code: {self.product_code}', 'Amount to pay/Paid: #{self.amount_paid}', 'Reference: {self.rave_ref}', 'Payment Status: {self.rave_status}')"


