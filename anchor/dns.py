from twisted.internet import protocol, defer
from twisted.names import dns, client, server, common
from twisted.python import failure


class LocalResolver(common.ResolverBase):
    """Resolver that returns nothing but 127.0.0.1 as A record."""

    def __init__(self, domain):
        common.ResolverBase.__init__(self)
        self.domain = domain

    def _lookup(self, name, cls=None, type=None, timeout=None):
        if name.endswith(self.domain):
            record = dns.Record_A("127.0.0.1")
            result = dns.RRHeader(name, dns.A, dns.IN, 3600, record)
            return defer.succeed(([result], [], []))
        return defer.fail(failure.Failure(dns.DomainError(name)))


dev_resolver = LocalResolver('dev')
resolver = client.Resolver('/etc/resolv.conf')
factory = server.DNSServerFactory([dev_resolver, resolver])
protocol = dns.DNSDatagramProtocol(factory)
