#!/usr/bin/env python

try:
    import hashlib
    md5_constructor = hashlib.md5
except ImportError:
    import md5
    md5_constructor = md5.new

import struct
from socket import socket, AF_INET, SOCK_DGRAM


GROWL_UDP_PORT = 9887
GROWL_PROTOCOL_VERSION = 1
GROWL_TYPE_REGISTRATION = 0
GROWL_TYPE_NOTIFICATION = 1


class GrowlSettings(object):

    def __init__(self, server, password, application=None, notification=None):

        self.server = server
        self.password = password
        if application:
            self.application = application
        else:
            self.application = 'rawr'

        if notification:
            self.notification = notification
        else:
            self.notification = 'default'


class GrowlRegistrationPacket(object):

    def __init__(self, application, password = None ):

        self.notifications = []
        self.defaults = []
        self.application = application.encode("utf-8")
        self.password = password

    def addNotification(self, notification, enabled=True):

        self.notifications.append(notification)

        if enabled:
            self.defaults.append(len(self.notifications)-1)

    def payload(self):

        self.data = struct.pack("!BBH", GROWL_PROTOCOL_VERSION,
                        GROWL_TYPE_REGISTRATION, len(self.application))

        self.data += struct.pack("BB", len(self.notifications),
                len(self.defaults))
        self.data += self.application

        for notification in self.notifications:
            encoded = notification.encode("utf-8")
            self.data += struct.pack("!H", len(encoded))
            self.data += encoded

        for default in self.defaults:
            self.data += struct.pack("B", default)

        self.checksum = md5_constructor()
        self.checksum.update(self.data)

        if self.password:
             self.checksum.update(self.password)

        self.data += self.checksum.digest()
        return self.data


class GrowlNotificationPacket(object):

    def __init__(self, application, notification, title, description,
            priority=0, sticky=False, password=None):

        self.application = application.encode("utf-8")
        self.notification = notification.encode("utf-8")
        self.title = title.encode("utf-8")
        self.description = description.encode("utf-8")
        self.password = password
        self.priority = priority
        self.sticky = sticky

    def payload(self):

        flags = (self.priority & 0x07) * 2

        if self.priority < 0:
            flags |= 0x08

        if self.sticky:
            flags = flags | 0x0100


        self.data = struct.pack( "!BBHHHHH", GROWL_PROTOCOL_VERSION,
                GROWL_TYPE_NOTIFICATION, flags, len(self.notification),
                len(self.title), len(self.description), len(self.application))

        self.data += self.notification
        self.data += self.title
        self.data += self.description
        self.data += self.application
        self.checksum = md5_constructor()
        self.checksum.update(self.data)

        if self.password:
             self.checksum.update(self.password)

        self.data += self.checksum.digest()

        return self.data


def growl_send(title, message, config, register=True):

    addr = (config.server, GROWL_UDP_PORT)
    s = socket(AF_INET,SOCK_DGRAM)

    p = GrowlRegistrationPacket(application="vagrant", password=config.password)
    p.addNotification("general", enabled=True)
    s.sendto(p.payload(), addr)

    p = GrowlNotificationPacket(application="vagrant",
        notification="general", title=title,
        description=message, priority=1,
        password=config.password)

    s.sendto(p.payload(),addr)
    s.close()
