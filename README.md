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
    ENV/bin/pip install -r requirements.txt
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
    /save

Finally;

    crontab -e
    
    @reboot screen -d -m irssi
    @reboot (cd /home/daniel/.irssi/irc2xmpp; ENV/bin/python relay_daemon.py config.yml)

This uses more than 0.0001% cpu! Unacceptable.
----------------------------------------------

Python likes polling condition variables. This patch reduces the symptoms.

Side effects: slow at shutting down, lag when sending messages (not really
important). Obviously only do this to the virtualenv that irc2xmpp uses because
it would probably mess up other software up badly.

    cp /usr/lib/python2.7/threading.py ENV/lib/python2.7/threading.py
    patch -d ENV -p1 < lowcpu.patch

Probably have to do it manually for other python versions.
