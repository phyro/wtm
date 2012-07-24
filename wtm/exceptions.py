
from wtm.helpers import PLAYER_PERM, ADMIN_PERM



class GameException(Exception):
    """Baseclass for all game exceptions."""

    name = None
    description = None
    permission = None

    def __init__(self, description=None, permission=None):
        if description != None:     #Needed to get the description
            self.description = description
        if permission != None:
            self.permission = permission
        self.name = self.__class__.__name__

    def get_description(self):
        """Returns the description of an exception."""
        return self.description

    def as_html(self):
        """Returns the html presentation of the exception."""
        return """
            <div id="exception">
                <div id="exception_name">
                    Name: %s
                </div>
                <div id="exception_description">
                    Description: %s
                </div>
            </div>

        """ % (self.name, self.description)

    def as_console_output(self):
        """Returns the output for console read."""
        return """Name:%s\nDescription:%s""" % (self.name, self.description)

class UnknownGameException(GameException):
    """Unknown game exception."""

    permission = PLAYER_PERM
    description = """
        Unknown game exception. What the heck happened?
    """

#----------------------------------------------------------------------------
#                            Player Exceptions
#----------------------------------------------------------------------------

class PlayerDoesNotExist(GameException):
    """Player does not exist exception."""

    permission = PLAYER_PERM
    description = """
        This player doesn't exist.
    """


#----------------------------------------------------------------------------
#                            Network Exceptions
#----------------------------------------------------------------------------

class NetworkBadRemoveInvite(GameException):
    """Could not remove invite from a network."""

    permission = PLAYER_PERM
    description = """
        Could not remove the invite. Player had no invitation.
    """

class NetworkBadAddPlayer(GameException):
    """Could not remove invite from a network."""

    permission = PLAYER_PERM
    description = """
        Could not add player. Test exception.
    """

class NetworkBadInvite(GameException):
    """Could not remove invite from a network."""

    permission = PLAYER_PERM
    description = """
        Could not remove the invite. Player had no invitation.
    """

class NetworkNotLeader(GameException):
    """Not the leader of the network exception."""

    permission = PLAYER_PERM
    description = """
        You are not the leader of the network.
    """

class NetworkAlreadyInNetwork(GameException):
    """Player is already in a network exception."""

    permission = PLAYER_PERM
    description = """
        This player is already in a network.
    """

class NetworkIsFull(GameException):
    """Network is full exception."""

    permission = PLAYER_PERM
    description = """
        This network is full.
    """

class NetworkDoesNotExist(GameException):
    """Network does not exist exception."""

    permission = PLAYER_PERM
    description = """
        This network does not exist.
    """

class NetworkNotInANetwork(GameException):
    """Player is not in a network exception."""

    permission = PLAYER_PERM
    description = """
        Player not in a network.
    """


#----------------------------------------------------------------------------
#                            Resources Exceptions
#----------------------------------------------------------------------------

class NotEnoughResources(GameException):
    """Player does not have enough resources."""

    permission = PLAYER_PERM
    description = """
        You dont have enough resources.
    """


#----------------------------------------------------------------------------
#                            Building Exceptions
#----------------------------------------------------------------------------

class BuildingRequirementsNotMet(GameException):
    """Player does not meet building requirements."""

    permission = PLAYER_PERM
    description = """
        You can't build this building yet.
    """



#All exceptions tupple
ALL_EXCEPTIONS = (
        #Base
        GameException,
        UnknownGameException,
        #Player
        PlayerDoesNotExist,
        #Network
        NetworkBadRemoveInvite,
        NetworkBadAddPlayer,
        NetworkBadInvite,
        NetworkNotLeader,
        NetworkAlreadyInNetwork,
        NetworkIsFull,
        NetworkDoesNotExist,
        #Resources
        NotEnoughResources,
        #Building
        BuildingRequirementsNotMet
)
