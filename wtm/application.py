from flask import Flask, session, g
from wtm.models import *
from wtm.views import frontend, admin, account, game
from wtm.database import db_session




def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.cfg')
    
    #Register blueprints
    app.register_blueprint(frontend)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(account, url_prefix='/account')
    app.register_blueprint(game, url_prefix='/game')
    
    
    #Configure close session
    configure_close_session(app)
    configure_before_handlers(app)
    
    return app



#-----------------Configurations--------------------

def configure_close_session(app):
    
    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()
        
        
def configure_before_handlers(app):
    
    #za vsak request dobi g.user ce je mogoce
    @app.before_request
    def getGUser():
        if session.has_key("username"):
            g.user = User.query.filter(User.username==session["username"]).first()
        else:
            g.user = None

    #za vsak request dobi g.game ce je mogoce
    @app.before_request
    def getGame():
        if session.has_key("cur_game") and session["cur_game"] != None:
            g.game = Game.query.filter(Game.id == session["cur_game"]).first()
        else:
            g.game = None
    