from flask import g, request, redirect, url_for, flash

#Globals
PLAYER_PERM = 100
ADMIN_PERM = 200


def get_player():
    """Returns the player object of the currect user and game he is in."""
    return g.user.get_player(g.game.id)

def flash_e(e, category):
    """Used to flash exceptions. Receives the exception and class category.
    Decides whether to flash exception or not, based on the permission of the user.
    """
    if g.user.permission >= e.permission:
        flash(u"%s" %(e.as_html()), category)
    else:
        flash(u"You do not have permission to see this exception.", "warning")
    