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


DEFAULT_TIMEOUT = 15  # seconds


def service_is_available(host, port):
    """
    Return True if the connection to the host and port is successful.

    @param host: str: hostname of the server
    @param port: int: TCP port to which to connect
    @return: bool
    """
    s = socket.socket()
    try:
        s.connect((host, port))
    except Exception:
        return False
    else:
        return True


def wait_for_service(host, port, timeout=DEFAULT_TIMEOUT):
    """
    Return True if connection to the host and port is successful within the timeout.

    @param host: str: hostname of the server
    @param port: int: TCP port to which to connect
    @param timeout: int: length of time in seconds to try to connect before giving up
    @return: bool
    """
    start = time.time()
    # could be a string
    timeout = int(timeout)
    while True:
        if service_is_available(host, port):
            return True
        else:
            if time.time() - start > timeout:
                return False
            else:
                time.sleep(1)


def main():
    args = sys.argv[1:]
    varname = os.getenv('URLWAIT_VARNAME', 'DATABASE_URL')
    timeout = os.getenv('URLWAIT_TIMEOUT', DEFAULT_TIMEOUT)
    if args:
        if args[0] in ('-h', '--help', '-?'):
            return __doc__
        service_url = args[0]
        if len(args) == 2:
            timeout = args[1]
    else:
        service_url = os.environ[varname]

    service = urlparse.urlparse(service_url)
    socket.setdefaulttimeout(int(timeout))

    if wait_for_service(service.hostname, service.port, timeout):
        return 0
    else:
        return 'Could not connect to {0} on port {1}'.format(service.hostname, service.port)


if __name__ == '__main__':
    sys.exit(main())
