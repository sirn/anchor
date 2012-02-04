DNS responder and port forwarding service

Port usage:
[29430] DNS responder
[29431] HTTP reverse proxy

Configuration:
Put site configuration file in .anchor/ directory in your home directory.

    [anchor]
    domain = anchor.dev
    aliases = www
    port = 3000

    [images]
    directory = /srv/http/anchor/images/

All anchor configuration must have [anchor] as a default section, which
will be mapped to naked domain. You can also provide alias if you want
to map to another subdomain.
