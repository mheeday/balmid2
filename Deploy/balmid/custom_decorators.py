from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from functools import wraps


def email_verifier(f):
    @wraps(f)
    def deco(*args, **kwargs):
        if not current_user.email_verified:
            flash("Your email isn't verified yet", 'info')
            return redirect(url_for("index"))

        return f(*args, **kwargs)
    return deco