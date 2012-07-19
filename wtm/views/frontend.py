from flask import Blueprint, request, url_for, redirect, g, session, flash, \
     abort, render_template, escape, jsonify

from jinja2 import TemplateNotFound

from wtm.forms import *     #Import forms
from wtm.models import *    #Import models
from wtm.database import db_session
from wtm.decorators import game_required

frontend = Blueprint('frontend', __name__)



@frontend.route("/", methods=("GET", "POST"))
def index():
    print "LALA2asdasda"
    all_games = Game.get_all_games()
    return render_template("index.html", all_games=all_games)


@frontend.route("/joingame/<int:game_id>", methods=("GET", "POST"))
def join_game(game_id):
    my_games = g.user.get_my_games()
    my_games_idxs = [cur_game.id for cur_game in my_games]
    if game_id in my_games_idxs:
        #You already joined... error
        flash(u"You already joined this game.")
        return redirect(url_for('frontend.index'))
        
    else:
        #Join the game
        g.user.join_game(game_id)
        flash(u"You successfully joined the game.")
        #Set active game to the game user joined
        session["cur_game"] = game_id
        return redirect(url_for('game.index'))


@frontend.route("/playgame/<int:game_id>", methods=("GET", "POST"))
def play_game(game_id):
    my_games = g.user.get_my_games()
    my_games_idxs = [cur_game.id for cur_game in my_games]
    if game_id in my_games_idxs:
        session["cur_game"] = game_id
        return redirect(url_for('game.index'))
    else:
        flash(u"You are not in this game.")
        return redirect(url_for('frontend.index'))
