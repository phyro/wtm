from flask import g, request, redirect, url_for

def get_player():
    return g.user.get_player(g.game.id)