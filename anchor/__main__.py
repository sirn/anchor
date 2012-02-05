from twisted.internet import reactor
from anchor import dns, http

reactor.listenUDP(29430, dns.protocol)
reactor.listenTCP(29430, dns.factory)
reactor.listenTCP(29431, http.site)
reactor.run()
