
from sqlalchemy import Column, Integer, String, func, or_, and_,ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from wtm.database import db_session, Base
from wtm.models.Game import Game, Network
from wtm.exceptions import NetworkNotLeader, NetworkAlreadyInNetwork, NetworkIsFull, PlayerDoesNotExist, \
                            NetworkDoesNotExist, UnknownGameException, \
                            ALL_EXCEPTIONS



class User(Base):
    """Defines a user. User can join a game (become a player)."""
    
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True)
    password = Column(String(120))  #TODO: hash password
    firstname = Column(String(120))
    lastname = Column(String(120))
    permission = Column(Integer)
    
    #relations
    players = relationship("Player", backref=backref('user'))   #User can have many players (on different servers)

    def __init__(self, username, password, firstname, lastname, permission):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.permission = permission

    def __repr__(self):
        return self.username
    
    #------------------------------------------------------------------------
    #                           User Methods
    #------------------------------------------------------------------------
    
    @classmethod
    def authenticate(self, username, password):
        """Returns a User object if authenticated, else None."""
        return User.query.filter(and_(User.username==username,User.password==password)).first()
    
    @classmethod
    def username_taken(self, username):
        """If username is taken returns False, else True."""
        return User.query.filter(User.username==username).first() != None
    
    def join_game(self, game_id):
        """Join a game with specified id and become a player in that game. Returns the new player."""
        #Get the game
        game = Game.query.filter(Game.id==game_id).first()
        
        #Create a new player
        new_player = Player(str(self.username))
        
        #Give user a player to play with
        self.players.append(new_player)
        db_session.add(self)
        db_session.commit()
        
        #Give game another player
        new_player = Player.query.filter(Player.id==new_player.id).first()
        game.players.append(new_player)
        db_session.add(game)
        db_session.commit()
        
        print "Joined the game: %s." % (game.name)
        return new_player
        
    def has_player(self, game_id):
        """Returns True if user has a player in a game with specified id."""
        return len([player for player in self.players if player.game_id == game_id]) == 1
    
    def get_my_games(self):
        """Returns a list of games i joined."""
        return [player.game for player in self.players]
    
    def get_player(self, game_id):
        """Returns user's player object for game with game_id."""
        player = [player for player in self.players if player.game_id == game_id]
        if len(player) == 0:
            return None
        else:
            return player[0]


class Player(Base):
    """Defines a Player. Player has resources, can build army, attack, etc."""
    
    __tablename__ = 'Player'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(120))
    
    #------------------------------------------------------------------------
    #                           Player Info
    #------------------------------------------------------------------------
    
    #Resources
    gold = Column(Integer)
    metal = Column(Integer)
    asteroids_free = Column(Integer)
    asteroids_gold = Column(Integer)
    asteroids_metal = Column(Integer)
    score = Column(Integer)
    
    #Building info    TODO
    
    #Research info    TODO
    
    #Army info        TODO
    
    #Attack info        TODO
    
    #Network info    TODO
    
    #Relations
    game_id = Column(Integer, ForeignKey('Game.id'))
    user_id = Column(Integer, ForeignKey('User.id'))
    network_id = Column(Integer, ForeignKey('Network.id'))
    
    
    
    def __init__(self, nickname):
        self.nickname = nickname
        self.gold = 0
        self.metal = 0
        self.asteroids_free = 0
        self.asteroids_gold = 0
        self.asteroids_metal = 0
        self.score = 0

    def __repr__(self):
        return self.nickname
    
    
    #------------------------------------------------------------------------
    #                           Player Methods
    #------------------------------------------------------------------------
    
    def get_buildings_built(self):
        """Returns a list of building that have been already built."""
        raise NotImplementedError, "Not yet..."
    
    def get_researches_done(self):
        """Returns a list of researches that have been already done."""
        raise NotImplementedError, "Not yet..."
    
    def get_my_attacks(self):
        """Returns a list of my attacks."""
        raise NotImplementedError, "Not yet..."
    
    def get_enemy_attacks(self):
        """Returns a list of attacks that are set on me."""
        raise NotImplementedError, "Not yet..."
    
    def get_nr_of_asteroids(self):
        """Returns the number of asteroids the player has."""
        return self.asteroids_free + self.asteroids_gold + self.asteroids_metal
    
    #---------------------------- Network Methods --------------------------------------
    
    def get_network_attacks(self):
        """Returns a list of attacks in whole my network."""
        #If player not in a network, error
        raise NotImplementedError, "Not yet..."
    
    
    def create_network(self, name):
        """Create a new network."""
        if self.network_id != None:
            raise NetworkAlreadyInNetwork
        else:
            new_network = Network(name, self.id)
            game = Game.query.filter(Game.id == self.game_id).first()
            game.networks.append(new_network)
            db_session.add(new_network)
            db_session.add(game)
            db_session.commit()
            
    
    def has_network(self):
        """Returns True if player is in a network."""
        return self.network_id != None
            
    def leave_network(self):
        """Make a player leave the network. If player is the leader... delete the network."""
        if self.network.leader_id == self.id:
            #If this player is the leader of the network remove all network players
            cur_network = Network.query.filter(Network.id == self.network_id).first()
            for network_player in cur_network.players:
                network_player.network_id = None
                db_session.add(network_player)
            #Remove also all network invites
            for invite in cur_network.invites:
                cur_network.invites.remove(invite)
            db_session.add(cur_network)
            db_session.delete(cur_network)
            db_session.commit()
            
        self.network_id = None
        db_session.add(self)
        db_session.commit()
        
    def invite_network(self, player_id):
        """Player invites another player in a network."""
        #Check if player inviting is the leader of the network
        network = Network.query.filter(Network.id == self.network_id).first()
        if network == None:
            raise NetworkDoesNotExist
        if network.leader_id != self.id:
            raise NetworkNotLeader
        
        #If it is, check if the invited player exists and is already in a network
        player = Player.query.filter(Player.id == player_id).first()
        if not player:
            raise PlayerDoesNotExist
        if player.has_network():
            raise NetworkAlreadyInNetwork
        
        #Check if network is full
        if network.is_full():
            raise NetworkIsFull
        
        #Everything appears ok, invite him
        network.invite(player_id)
    
    def join_network(self, network_id):
        """Player joins a network with specified id."""
        network = Network.query.filter(Network.id == network_id).first()
        #If player is in a network, he can't join
        if self.has_network():
            raise NetworkAlreadyInNetwork
            #return (False, u"You are already in a network and can't join one")
        #Check if network is full
        if network.is_full():
            raise NetworkIsFull
            #return (False, u"Your network is full")
        
        try:
            network.add_player(self.id)
        except ALL_EXCEPTIONS as e:
            raise e
        
    def deny_network(self, network_id):
        """Player denies an invitation to join a network."""
        try:
            network = Network.query.filter(Network.id == network_id).first()
            self.invites.remove(network)
            db_session.add(self)
            db_session.commit()
        except:
            raise UnknownGameException
        
    def deny_all_network_invites(self):
        """Removes all network invites players had pending."""
        try:
            for invite in self.invites:
                self.invites.remove(invite)
        except:
            raise UnknownGameException