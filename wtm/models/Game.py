
from sqlalchemy import Column, Integer, String, func, or_, and_,DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from wtm.database import db_session, Base
import datetime





class Game(Base):
    """Defines a game. A game has start date, end date, players, etc."""
    
    __tablename__ = 'Game'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    tick = Column(Integer)  #Tick in seconds
    max_network_size = Column(Integer)  #Max nr of players in a network
    
    #------------------------------------------------------------------------
    #                           Game Info
    #------------------------------------------------------------------------
    
    players = relationship("Player", backref=backref('game'))
    networks = relationship("Network", backref=backref('game'))
    
    def __init__(self, name, tick, start_date, end_date, max_network_size=5):
        self.name = name
        self.tick = tick
        self.start_date = start_date
        self.end_date = end_date
        self.max_network_size = max_network_size

    def __repr__(self):
        return self.name
    
    #------------------------------------------------------------------------
    #                           Game Methods
    #------------------------------------------------------------------------
    
    @classmethod
    def get_all_games(cls):
        """Returns a list of all games."""
        return Game.query.all()
    
    def get_top100(self):
        """Returns a list of top100 players."""
        return sorted(self.players, key=lambda x: x.score)[:100]
    
    def get_top10_networks(self):
        """Returns a list of top10 networks."""
        return sorted(self.networks, key=lambda x: sum([cur_player.score for cur_player in x.players]))[:10]
    
class Network(Base):
    """Defines a network of players."""
    
    __tablename__ = 'Network'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    leader_id = Column(Integer)
    
    players = relationship("Player", backref=backref('network'))
    game_id = Column(Integer, ForeignKey('Game.id'))
    
    #------------------------------------------------------------------------
    #                           Network Info
    #------------------------------------------------------------------------
    
    
    def __init__(self, name, leader_id):
        self.name = name
        self.leader_id = leader_id
        self.add_player(leader_id)

    def __repr__(self):
        return self.name
    
    #------------------------------------------------------------------------
    #                           Network Methods
    #------------------------------------------------------------------------
    
    
    def add_player(self, player_id):
        """Adds a player to the network (if possible)."""
        #TODO: Check if that player even exists.
        #TODO: SERIOUSLY? YOU'LL RETURN STRINGS? LOL NOOB.
        network_players = [player.id for player in self.players]
        if player_id not in network_players:
            from wtm.models.User import Player  #TODO: VERY UGLY; DAMN CIRCULAR IMPORTS. REFACTOR? :O
            new_player = Player.query.filter_by(id = player_id).first()
            self.players.append(new_player)
            db_session.add(self)
            db_session.commit()
            return (True, "")
        else:
            return (False, "Already in a network")
    
    def get_score(self):
        """Returns a score of the network."""
        return sum( [player.score for player in self.players] )


