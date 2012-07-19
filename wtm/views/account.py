from flask import Blueprint, request, url_for, redirect, g, session, flash, \
     abort, render_template

from jinja2 import TemplateNotFound

from wtm.forms import *     #Import forms
from wtm.models import *    #Import models


account = Blueprint('account', __name__)

"""
@frontend.route('/', defaults={'page': 'index'})
@frontend.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)
"""

@account.route("/login", methods=("GET", "POST"))
def login():
    
    form_login = LoginForm()
    
    if form_login.validate_on_submit():
        user = User.authenticate(form_login.login.data,
                             form_login.password.data)
        if user:
            #session.permanent = form.remember.data
            
            #identity_changed.send(current_app._get_current_object(),
            #                      identity=Identity(user.id))
            session["username"] = user.username
            g.user = user
            session["cur_game"] = None #Trenutno ni v nobeni izmed iger
            g.game = None
            """
            # check if openid has been passed in
            openid = session.pop('openid', None)
            if openid:
                user.openid = openid
                db.session.commit()
                
                flash(_("Your OpenID has been attached to your account. "
                      "You can now sign in with your OpenID."), "success")


            else:
                flash(_("Welcome back, %(name)s", name=user.username), "success")

            next_url = form.next.data

            if not next_url or next_url == request.path:
                next_url = url_for('user.posts', username=user.username)

            return redirect(next_url)
            """
            flash("You have successfuly logged in %s" % user.username, "msgText")
            next_url = url_for('frontend.index')
            return redirect(next_url)
        else:

            flash("Sorry, invalid login", "errorText")
    
    #flash(u'Login form set.', 'green')
    return render_template('account/login.html', form_login=form_login)

@account.route("/logout/", methods=("GET", "POST"))
def logout():
    
    session.pop('username', None)
    flash('You were logged out', "msgText")
    return redirect(url_for('frontend.index'))