# WHAT IS ANCHOR?

Anchor is [Pow](http://pow.cx/)-like DNS responder and port forwarding service. Unlike Pow, Anchor does not have a built-in webserver and won't launch web process for you. You have to run your own development webserver and Anchor will simply forward all requests from `.dev` domain to any port you defined.

# INSTALLATION

Installing Anchor is still somewhat complex at its current state. If you feel advantageous enough, you may follow these instructions. Please make sure you have Python 2.6 (or higher) and [pip](http://www.pip-installer.org/en/latest/index.html) installed on your system.

Anchor is targeted for Mac OS X but may also work with other UNIX-like systems (you have to use `127.0.0.1:29430` as a DNS server and forward port 80 to 29431).

Try it at your own risk.

## Installation on Mac OS X

1. `pip install git+https://github.com/sirn/anchor.git`
2. Create `/etc/resolvers/dev` with following contents:

        nameserver 127.0.0.1
        port 29430

    Pow users may have this file created, if you no longer use Pow you can delete it.

3. In your **root directory** create `/Library/LaunchDaemons/com.gridth.anchorconfig.plist` with following contents:

        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.gridth.anchorconfig</string>
            <key>ProgramArguments</key>
            <array>
                <string>sh</string>
                <string>-c</string>
                <string>ipfw add fwd 127.0.0.1,29431 tcp from any to me dst-port 80 in &amp;&amp; sysctl -w net.inet.ip.forwarding=1</string>
            </array>
            <key>UserName</key>
            <string>root</string>
            <key>RunAtLoad</key>
            <true />
        </dict>
        </plist>

4. In your **home directory** create `~/Library/LaunchAgents/com.gridth.anchor.plist` with following contents:

        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist>
        <dict>
            <key>Label</key>
            <string>com.gridth.anchor</string>
            <key>ProgramArguments</key>
            <array>
                <string>python</string>
                <string>-m</string>
                <string>anchor</string>
            </array>
            <key>KeepAlive</key>
            <true />
            <key>RunAtLoad</key>
            <true />
        </dict>
        </plist>

    You may want to change `<string>python</strong>` if you're using VirtualEnv.

5. Run `launchctl load -w /Library/LaunchDaemons/com.gridth.anchorconfig.plist` and `launchctl load -w ~/Library/LaunchAgents/com.gridth.anchor.plist`.

# USAGE

Put a site configuration file in `.anchor/` directory in your home directory. The configuration file must have at least `[anchor]` declared. For example:

    [anchor]
    aliases = www
    port = 3000

    [images]
    directory = /srv/http/anchor/images/

Everything in anchor section are mapped to naked domain using filename as its domain: `[anchor]` section in `mysite.conf` is mapped to `mysite.dev`, for example. You may also create subdomain with a new section (in the example above `images.mysite.dev` will serve static contents from `directory`) or aliases using `aliases` directive.

Currently there are three directives available:

* `aliases` space-separated list of subdomain aliases.
* `port` specify port to to forward.
* `directory` serve static content from the following directory.

`directory` directive and `port` directive can't be used together.

# NOTES

Port usage:

* `29430` DNS responder
* `29431` HTTP reverse proxy

Distributed under MIT license.
