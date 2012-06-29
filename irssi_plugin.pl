# Based on hilightwin by Timo Sirainen http://static.quadpoint.org/irssi/

use Irssi;
use IO::Socket::UNIX;

use vars qw($VERSION %IRSSI); 
$VERSION = "0.01";

%IRSSI = (
    authors	=> "Daniel Richman"
    contact	=> "main\@danielrichman.co.uk"
    name	=> "irc2xmpp",
    description	=> "Forward hilighted messages to XMPP",
    license	=> "Public Domain",
    url		=> "http://irssi.org/",
    changed	=> "2012-06-29T17:23:00+0100"
);

my $client_sock = IO::Socket::UNIX->new (Type => SOCK_DGRAM);
my $setting_name = $IRSSI{'name'} . '_socket'
Irssi::settings_add_str('misc', $setting_name, "relay_sock");

sub sig_printtext {
  my ($dest, $text, $stripped) = @_;

  # change to (MSGLEVEL_HILIGHT|MSGLEVEL_MSGS) to work for
  # all privmsgs too
  if (($dest->{level} & (MSGLEVEL_HILIGHT)) &&
      ($dest->{level} & MSGLEVEL_NOHILIGHT) == 0) {
    if ($dest->{level} & MSGLEVEL_PUBLIC) {
      $text = $dest->{target}.": ".$text;
    }
    $text =~ s/%/%%/g;

    my $server_sock = Irssi::settings_get_str($setting_name);
    send($client_sock, $text, 0, $server_sock);
  }
}

Irssi::signal_add('print text', 'sig_printtext');
