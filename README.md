irc2xmpp
========

Wat?
----

Highlighted messages are sent to an XMPP account. Phone vibrates/popup on
desktop. Win.

Perl script dumps highlighty messages into a UNIX socket; a python daemon
listens to this and then passes them on via XMPP/Jabber to the target.
This was easier because I suck at perl, integrating XMPP to irssi's event
loop is a pain and starting a thread in a plugin is evil.

Install
-------

    cd ~/.irssi
    git clone git://github.com/danielrichman/irc2xmpp.git
    cd irc2xmpp
    virtualenv ENV
    (ENV/bin/activate; pip install -r requirements.txt)
    cp relay_config.yml config.yml

Create a random google account for the xmpp bot, and add the address (JID) and
password to config.yml. Target is the person that the messages will be sent to
and should probably be added as a google talk friend.

Set log filename and socket in config.yml:

    logging:
        level: WARNING
        filename: /home/daniel/.irssi/irc2xmpp/relay.log
    socket: /home/daniel/.irssi/irc2xmpp/relay_sock

Install plugin

    cd ~/.irssi/scripts/autorun
    ln -s ../../irc2xmpp/irssi_plugin.pl

In irssi:

    /load irc2xmpp
    /set irc2xmpp_socket /home/daniel/.irssi/irc2xmpp/relay_sock
    /set

Finally;

    crontab -e
    
    @reboot screen -d -m irssi
    @reboot (cd /home/daniel/.irssi/irc2xmpp; ENV/bin/python relay_daemon.py config.yml)

