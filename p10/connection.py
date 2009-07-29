#!/usr/bin/env python

class Connection:
    """ Represents a connection upstream, and holds the configuration values for this server """
    
    numericID = None
    serverName = None
    networkName = None
    adminNick = None
    contactEmail = None
    
    def sendLine(self, source_client, token, args):
        """ Send a line upsteam. This is also parsed by us, to maintain state.
        
            source_client: An integer, or None, representing which client is sending this message
            token: The token to be sent.
            args: An array of strings making up the message body """
        pass

class ConnectionError(Exception):
    """ When an error occurs in a connection """
    pass