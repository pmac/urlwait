#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:

    $ urlwait [SERVICE URL] [TIMEOUT]

    SERVICE URL is a connection url, e.g. a typical value for $DATABASE_URL. TIMEOUT is
    a number of seconds to try to connect to the host and port specified in the SERVICE
    URL. These values may also be specified in environment variables, but command line
    args take precedence:

        URLWAIT_VARNAME: the env var name containing the URL to check. Default DATABASE_URL.
        URLWAIT_TIMEOUT: the number of seconds to wait. Default 15.

    Returns a 0 status if the connection completed successfully before the timeout, or 1 if not.
    It is designed for use with Docker or other dev or testing environments where the connected
    services and the app are started simultaneously, but one should wait for the other.

Examples:

    The following are equivalent:

    $ urlwait redis://localhost:6379/0 20
    $ urlwait $CACHE_URL 20
    $ URLWAIT_VARNAME=CACHE_URL URLWAIT_TIMEOUT=20 urlwait
"""

from __future__ import unicode_literals, print_function

import os
import socket
import sys
import time

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


__all__ = ['wait_for_service', 'wait_for_url']
DEFAULT_TIMEOUT = 15  # seconds
DEFAUTL_PORTS = {
    'amqp': 5672,
    'http': 80,
    'https': 443,
    'mysql': 3306,
    'mysql2': 3306,
    'pgsql': 5432,
    'postgres': 5432,
    'postgresql': 5432,
    'redis': 6379,
    'hiredis': 6379,
}


class ServiceURL(object):
    host = None
    port = None
    scheme = None

    def __init__(self, url, timeout=DEFAULT_TIMEOUT):
        self.timeout = int(timeout)
        service = urlparse.urlparse(url)
        self.scheme = service.scheme
        self.host = service.hostname
        self.port = service.port or DEFAUTL_PORTS.get(service.scheme, None)

    def is_available(self):
        """
        Return True if the connection to the host and port is successful.

        @return: bool
        """
        if not self.port:
            raise RuntimeError('port is required')

        s = socket.socket()
        try:
            s.connect((self.host, self.port))
        except Exception:
            return False
        else:
            return True

    def wait(self):
        start = time.time()
        # could be a string
        while True:
            if self.is_available():
                return True
            else:
                if time.time() - start > self.timeout:
                    return False
                else:
                    time.sleep(1)


def wait_for_service(host, port, timeout=DEFAULT_TIMEOUT):
    """
    Return True if connection to the host and port is successful within the timeout.

    @param host: str: hostname of the server
    @param port: int: TCP port to which to connect
    @param timeout: int: length of time in seconds to try to connect before giving up
    @return: bool
    """
    service = ServiceURL('tcp://{}:{}'.format(host, port), timeout)
    return service.wait()


def wait_for_url(url, timeout=DEFAULT_TIMEOUT):
    """
    Return True if connection to the host and port specified in url
    is successful within the timeout.

    @param url: str: connection url for a TCP service
    @param timeout: int: length of time in seconds to try to connect before giving up
    @raise RuntimeError: if no port is given or can't be guessed via the scheme
    @return: bool
    """
    service = ServiceURL(url, timeout)
    return service.wait()


def main(args=None):
    args = args or sys.argv[1:]
    varname = os.getenv('URLWAIT_VARNAME', 'DATABASE_URL')
    timeout = os.getenv('URLWAIT_TIMEOUT', DEFAULT_TIMEOUT)
    if args:
        if args[0] in ('-h', '--help', '-?'):
            return __doc__
        service_url = args[0]
        if len(args) == 2:
            timeout = args[1]
    else:
        try:
            service_url = os.environ[varname]
        except KeyError:
            return 'Environment variable {0} not found'.format(varname)

    socket.setdefaulttimeout(int(timeout))
    service = ServiceURL(service_url, timeout)
    try:
        if service.wait():
            return 0
        else:
            return 'Could not connect to {0}'.format(service_url)
    except RuntimeError:
        return 'Could not guess port for {}'.format(service.scheme)


if __name__ == '__main__':
    sys.exit(main())
