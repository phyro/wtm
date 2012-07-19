from flask import Blueprint, request, url_for, redirect, g, session, flash, \
     abort, render_template

from jinja2 import TemplateNotFound

from wtm.forms import *     #Import forms
from wtm.models import *    #Import models
from wtm.database import db_session

admin = Blueprint('admin', __name__)


@admin.route("/")
def index():
    
    return render_template('new_advice.html')




