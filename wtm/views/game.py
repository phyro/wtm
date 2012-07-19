from flask import Blueprint, request, url_for, redirect, g, session, flash, \
     abort, render_template, escape, jsonify

from jinja2 import TemplateNotFound

from wtm.forms import *     #Import forms
from wtm.models import *    #Import models
from wtm.database import db_session
from wtm.decorators import game_required
from wtm.helpers import get_player

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
            flash(u"Network was successfully created.", "notice")
            return redirect(url_for('game.network'))
        else:
            #Else, print the error
            flash(u"%s"%(err), "warning")
            return render_template("game/network/create.html", form=form)

    else:
        return render_template("game/network/create.html", form=form)
    

@game.route("/network_invite/<int:player_id>", methods=("GET", "POST"))
@game_required
def network_invite(player_id):
    """Player (leader of a network) sends an invite to another player."""
    player = g.user.get_player(g.game.id)
    status, err = player.invite_network(player_id)
    if status:
        flash(u"You have successfully invited a player to join your network.", "notice")
    else:
        flash(u"An error occured: %s" %(err), "warning")
    
    return redirect(url_for("game.network"))


@game.route("/network_invite_accept/<int:network_id>", methods=("GET", "POST"))
@game_required
def network_invite_accept(network_id):
    """Player accepts an invite and joins a network."""
    player = g.user.get_player(g.game.id)
    status, err = player.join_network(network_id)
    if status:
        flash(u"You have successfully invited a player to join your network.", "notice")
    else:
        flash(u"An error occured: %s" %(err), "warning")
    
    return redirect(url_for("game.network"))


@game.route("/network_invite_deny/<int:network_id>", methods=("GET", "POST"))
@game_required
def network_invite_deny(network_id):
    """Player denies an invite to join a network."""
    player = get_player()
    status, err = player.deny_network(network_id)
    if status:
        flash(u"You have successfully denied an invitation to join a network.", "notice")
    else:
        flash(u"An error occured: %s" %(err), "warning")
    
    return redirect(url_for("game.network"))
