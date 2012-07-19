# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, HiddenField, BooleanField, TextField, \
        PasswordField, SubmitField, TextField, RecaptchaField, \
        ValidationError, required, email, equal_to, regexp
        
        



class LoginForm(Form):
    
    remember = BooleanField(u"Remember me")
    
    login = TextField(u"Uporabniško ime:", validators=[
                      required(message=\
                               u"Uporabniško ime mora biti vneseno.")])

    password = PasswordField(u"Geslo:")

    submit = SubmitField(u"Prijava")