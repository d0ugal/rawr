rawr
====================

A python network interface and command line utility for sending growl 
notifications to a OSX host.

Initially I created this to allow me to send growl notifications from virtual
machines running on my MacBook.

Setup
====================

For this to work, you need to enable 'Listen for incoming notifications' and
'Allow remote application registration' under the network tab in your growl 
settings.


Usage
====================

Usage: rawr [options]

Options:
  -h, --help            show this help message and exit
  -t TITLE, --title=TITLE
                        Growl notification title.
  -m MESSAGE, --message=MESSAGE
                        Growl notification message.
  -s SERVER, --server=SERVER
                        Growl host server name or IP.
  -p PASSWORD, --password=PASSWORD
                        Growl server password.
  -a APPLICATION, --application=APPLICATION
                        Growl application name.
  -n NOTIFICATION, --notification=NOTIFICATION
                        Growl application notification name.
  -r REGISTER, --register=REGISTER
                        Should rawr attempt to register the application?

    ::
    rawr -s server -p password -a app -n notification -t title -m message


Copyright
====================

Base work is copyrighted by:

- netgrowl.py::

    netgrowl.py -  Growl 0.6 Network Protocol Client for Python
    Copyright (C) 2004 Rui Carmo. Code under BSD License.
    Author: Rui Carmo (http://the.taoofmac.com)
    Contributors: Ingmar J Stein (Growl Team)
    http://dailyconfig.googlecode.com/svn-history/r758/trunk/mytools/netgrowl.py

