from flask import Blueprint, request, url_for, redirect, g, session, flash, \
     abort, render_template, escape, jsonify

from jinja2 import TemplateNotFound

from wtm.forms import *     #Import forms
from wtm.models import *    #Import models
from wtm.database import db_session
from wtm.decorators import game_required

game = Blueprint('game', __name__)



@game.route("/", methods=("GET", "POST"))
@game_required
def index():
    """Renders game's main page... the top100."""
    return render_template("game/top100.html")


#-------------------------------------------------------------
#                        Network
#-------------------------------------------------------------

@game.route("/network", methods=("GET", "POST"))
@game_required
def network():
    """Renders game's network page."""
    return render_template("game/network/index.html")

@game.route("/network_leave", methods=("GET", "POST"))
@game_required
def network_leave():
    """Player leaves a network."""
    player = g.user.get_player(g.game.id)
    
    if not player.has_network():
        flash(u"Player does not have a network.")
        return redirect(url_for("game.index"))
    else:
        player.leave_network()
        flash(u"You have left the network.")
        return redirect(url_for("game.index"))
    
@game.route("/network_create", methods=("GET", "POST"))
@game_required
def network_create():
    """Player creates a new network."""
    player = g.user.get_player(g.game.id)
    if player.has_network():
        flash(u"Player already has a network.")
        return redirect(url_for("game.index"))
    
    form = NetworkCreateForm()
    
    if form.validate_on_submit():
        
        status, err = player.create_network(form.name.data)
        if status:
            #If network was created
            flash(u"Network was successfully created.", "msgText")
            return redirect(url_for('game.network'))
        else:
            #Else, print the error
            flash(u"%s"%(err), "errorText")
            return render_template("game/network/create.html", form=form)

    else:
        return render_template("game/network/create.html", form=form)
    

@game.route("/network_join_request/<int:network_id>", methods=("GET", "POST"))
@game_required
def network_join_request(network_id):
    """Player sends a request to the network leader."""
    player = g.user.get_player(g.game.id)
    if player.has_network():
        flash(u"Player already has a network.")
        return redirect(url_for("game.index"))
    
    form = NetworkCreateForm()
    
    if form.validate_on_submit():
        
        status, err = player.create_network(form.name.data)
        if status:
            #If network was created
            flash(u"Network was successfully created.", "msgText")
            return redirect(url_for('game.network'))
        else:
            #Else, print the error
            flash(u"%s"%(err), "errorText")
            return render_template("game/network/create.html", form=form)

    else:
        return render_template("game/network/create.html", form=form)
    
