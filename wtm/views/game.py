from flask import Blueprint, request, url_for, redirect, g, session, flash, \
     abort, render_template, escape, jsonify

from jinja2 import TemplateNotFound

from wtm.forms import *     #Import forms
from wtm.models import *    #Import models
from wtm.database import db_session
from wtm.decorators import game_required
from wtm.helpers import get_player, flash_e
from wtm.exceptions import ALL_EXCEPTIONS, NetworkAlreadyInNetwork, NetworkNotInANetwork

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
        flash_e(NetworkNotInANetwork, "warning")
        return redirect(url_for("game.index"))
    else:
        player.leave_network()
        flash(u"You have left the network.", "notice")
        return redirect(url_for("game.index"))
    
@game.route("/network_create", methods=("GET", "POST"))
@game_required
def network_create():
    """Player creates a new network."""
    player = g.user.get_player(g.game.id)
    if player.has_network():
        flash_e(NetworkAlreadyInNetwork, "warning")
        return redirect(url_for("game.index"))
    
    form = NetworkCreateForm()
    
    if form.validate_on_submit():
        
        try:
            player.create_network(form.name.data)
            flash(u"Network was successfully created.", "notice")
            return redirect(url_for('game.network'))
        except ALL_EXCEPTIONS as e:
            flash_e(e, "warning")
            return render_template("game/network/create.html", form=form)
    
    else:
        return render_template("game/network/create.html", form=form)
    

@game.route("/network_invite/<int:player_id>", methods=("GET", "POST"))
@game_required
def network_invite(player_id):
    """Player (leader of a network) sends an invite to another player."""
    player = g.user.get_player(g.game.id)
    try:
        player.invite_network(player_id)
        flash(u"You have successfully invited a player to join your network.", "notice")
    except ALL_EXCEPTIONS as e:
        flash_e(e, "warning")
    
    return redirect(url_for("game.network"))


@game.route("/network_invite_accept/<int:network_id>", methods=("GET", "POST"))
@game_required
def network_invite_accept(network_id):
    """Player accepts an invite and joins a network."""
    player = g.user.get_player(g.game.id)
    try:
        player.join_network(network_id)
        flash(u"You have successfully joined a network.", "notice")
    except ALL_EXCEPTIONS as e:
        flash_e(e, "warning")
    
    return redirect(url_for("game.network"))


@game.route("/network_invite_deny/<int:network_id>", methods=("GET", "POST"))
@game_required
def network_invite_deny(network_id):
    """Player denies an invite to join a network."""
    player = get_player()
    try:
        player.deny_network(network_id)
        flash(u"You have successfully denied an invitation to join a network.", "notice")
    except ALL_EXCEPTIONS as e:
        flash_e(e, "warning")
    
    return redirect(url_for("game.network"))
