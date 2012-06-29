# irc2xmpp.pl
# Based on hilightwin by Timo Sirainen http://static.quadpoint.org/irssi/

use Irssi;
use IO::Socket::UNIX;

use vars qw($VERSION %IRSSI); 
$VERSION = "0.01";

%IRSSI = (
    authors	=> "Daniel Richman",
    contact	=> "main\@danielrichman.co.uk",
    name	=> "irc2xmpp",
    description	=> "Forward hilighted messages to XMPP",
    license	=> "Public Domain",
    url		=> "http://irssi.org/",
    changed	=> "2012-06-29T17:23:00+0100"
);

$setting_name = $IRSSI{'name'} . '_socket';
Irssi::settings_add_str('misc', $setting_name, "relay_sock");

sub sig_printtext {
  my ($dest, $text, $stripped) = @_;

  if (($dest->{level} & (MSGLEVEL_HILIGHT|MSGLEVEL_MSGS)) &&
      ($dest->{level} & MSGLEVEL_NOHILIGHT) == 0) {
    if ($dest->{level} & MSGLEVEL_PUBLIC) {
      $stripped = $dest->{target}.": ".$stripped;
    }

    my $sock = IO::Socket::UNIX->new(
        Type => SOCK_DGRAM,
        Peer => Irssi::settings_get_str($setting_name)
    );
    send($sock, $stripped, 0);
  }
}

Irssi::signal_add('print text', 'sig_printtext');
