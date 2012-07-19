# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, HiddenField, BooleanField, TextField, \
        PasswordField, SubmitField, TextField, RecaptchaField, \
        ValidationError, required, email, equal_to, regexp
        
        



class NetworkCreateForm(Form):
    
    
    name = TextField(u"Network name:", validators=[
                      required(message=\
                               u"A network needs a name...")])
    
    submit = SubmitField(u"Create")