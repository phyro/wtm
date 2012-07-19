from functools import wraps
from flask import g, request, redirect, url_for

def game_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.game is None or g.user is None:    #If the game or user is not defined... hacking or bug?
            print "ni g.game ali g.user..."
            return redirect(url_for('frontend.index'))
        print "game_id:",g.game.id
        return f(*args, **kwargs)
    return decorated_function
