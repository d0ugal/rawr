from optparse import OptionParser

from rawr.network import growl_send, GrowlSettings

def main():

    usage = """rawr -s server -p password -t title -m message"""

    parser = OptionParser(usage)
    parser.add_option("-t", "--title", dest="title",
            help="Growl notification title.")
    parser.add_option("-m", "--message", dest="message",
            help="Growl notification message.")

    parser.add_option("-s", "--server", dest="server",
            help="Growl host server name or IP.")
    parser.add_option("-p", "--password", dest="password",
            help="Growl server password.")

    parser.add_option("-a", "--application", dest="application",
            help="Growl application name.", default="rawr",)
    parser.add_option("-n", "--notification", dest="notification",
            help="Growl application notification name.", default="default",)

    parser.add_option("-r", "--register", dest="register", default=True,
            help="Should rawr attempt to register the application?",)

    (options, args) = parser.parse_args()

    config = GrowlSettings(server=options.server, password=options.password,
        application=options.application, notification=options.notification)

    for attr in ['server', 'password', 'title', 'message']:
        if not getattr(options, attr):
            print "The '%s' arguement is required. See `rawr --help`" % attr
            return

    growl_send(options.title, options.message, config)
