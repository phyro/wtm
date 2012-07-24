import threading
import time


class Ticker(threading.Thread):
    """Defines a ticker for a game."""

    def __init__(self, tick_time, game_id):
        self.tick_time = tick_time  #In seconds
        self.game_id = game_id


    def run(self):
        """Runs the ticker."""
        while True:
            self.make_tick()
            print "MADE A TICK!"
            time.sleep(self.tick_time)

    def make_tick(self):
        """Makes a tick, updates every player."""
        #Get the game
        from wtm.models import Game #Would not work if imported at top
        game = Game.query.filter(Game.id == int(self.game_id)).first()
        #Go through all players in that game
        for player in game.players:
            player.ticker_update()




