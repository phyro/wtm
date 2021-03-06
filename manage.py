from flask.ext.script import Manager
from wtm.models import *
from wtm import create_app
from wtm.database import Base, engine, db_session
from wtm.helpers import PLAYER_PERM, ADMIN_PERM
from wtm.exceptions import ALL_EXCEPTIONS
from wtm.logic import Ticker

import datetime
from threading import Thread


app = create_app()
manager = Manager(app)


@manager.command
def initdb():
    """Creates all database tables."""
    Base.metadata.create_all(bind=engine)


    admin = User("admin", "admin", "boris", "bogdanovich", ADMIN_PERM)
    test_user = User("primi", "primi", "milivoj", "novakovic", PLAYER_PERM)
    test_user2 = User("tomi", "tomi", "milivoj", "novakovic", PLAYER_PERM)
    db_session.add(admin)
    db_session.add(test_user)
    db_session.add(test_user2)
    db_session.commit()

    #Create a game
    start_date = datetime.datetime.now()
    end_date = start_date + datetime.timedelta(1*365/12)    #1 Month game
    print "start_date:",start_date
    print "end_date:", end_date
    #end_date = datetime.datetime.
    game = Game("server1", 10, start_date, end_date)
    game2 = Game("server2", 60, start_date, end_date)
    db_session.add(game)
    db_session.add(game2)
    db_session.commit()


    #Add test_user to game
    p1 = test_user.join_game(game.id)
    p2 = test_user2.join_game(game.id)

    #Print all games and its players
    all_games = Game.query.all()
    for cur_game in all_games:
        print "Game: %s" % (cur_game.name)
        for player in cur_game.players:
            print "\t",player


    #Make a network
    try:
        p2.create_network(u"Testna zveza")
    except ALL_EXCEPTIONS as e:
        print e.as_console_output()



@manager.command
def dropdb():
    """Drops all database tables."""
    Base.metadata.drop_all(bind=engine)


@manager.option('-g', '--game', dest="game_id", required=True)
def ticker(game_id):
    """Starts a ticker for a specified game."""
    game = Game.query.filter(Game.id == int(game_id)).first()
    ticker_game1 = Ticker(game.tick, game_id)
    ticker_game1.run()


@manager.option('-u', '--username', dest="username", required=False)
@manager.option('-p', '--password', dest="password", required=False)
#@manager.option('-e', '--email', dest="email", required=False)
#@manager.option('-r', '--role', dest="role", required=False)
def create_user(username=None, password=None):
    """Creates new user, needs -u, -p parameters
    """

    if (username and password) and not User.username_taken(username):
        user = User(username,password)
        db_session.add(user)
        db_session.commit()

        print "added user with id:", user.id

    else:
        print "error, username taken or not enough params"



if __name__ == '__main__':
    manager.run()
