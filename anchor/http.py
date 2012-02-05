import os
from ConfigParser import SafeConfigParser
from twisted.internet import reactor, defer
from twisted.web import resource, server, proxy, static
from twisted.python import filepath
from anchor.utils import rrsplit


class WebResource(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)

    def getChild(self, path, request):
        return WebResource()

    def render(self, request):
        subdomain, domain, tld = rrsplit(request.getHeader("host"), ".", 2)
        config_path = os.path.expanduser("~/.anchor/%s.conf" % domain)

        # Config parser will contain empty dataset if file in config path
        # doesn't exist; we can simplify error handling to just [anchor]
        # section check.
        parser = SafeConfigParser()
        parser.read(config_path)
        if not parser.has_section("anchor"):
            return "Not configured"

        mappings = {None: "anchor"}
        for section in parser.sections():
            mappings[section] = section
            if not parser.has_option(section, "aliases"):
                continue
            for alias in parser.get(section, "aliases").split():
                mappings[alias] = section

        section = mappings.get(subdomain)
        if section is None:
            return "Subdomain %s is not defined." % subdomain

        # Currently supported two type of configuration
        # port      | forward request to port (via ProxyClientFactory)
        # directory | serving static files inside directory
        if parser.has_option(section, "port"):
            port = parser.getint(section, "port")
            request.content.seek(0, 0)
            reactor.connectTCP("127.0.0.1", port, proxy.ProxyClientFactory(
                request.method, request.uri, request.clientproto,
                request.getAllHeaders(), request.content.read(), request))
            return server.NOT_DONE_YET

        # TODO: feels somewhat hacky
        elif parser.has_option(section, "directory"):
            path = parser.get(section, "directory")
            site = static.File(path, defaultType="text/plain")
            for child in request.uri.split("/")[1:]:
                site = site.getChild(child, request)
            return site.render(request)

        return "Unknown target."


site = server.Site(WebResource())
