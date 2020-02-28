=======
URLWait
=======

.. image:: https://img.shields.io/travis/pmac/urlwait.svg
   :target: https://travis-ci.org/pmac/urlwait/
.. image:: https://img.shields.io/pypi/v/urlwait.svg
   :target: https://pypi.python.org/pypi/urlwait

I needed a way to block my app from starting until the database service was running and
accepting connections. This was particularly a problem when using Docker and docker-compose.
You can run this utility as part of a ``run-dev.sh`` or ``run-tests.sh`` script and it will
block for 15 seconds (configurable) until it can connect to the hostname and port as specified
in your connection URL (gleaned from DATABASE_URL environment variable by default).

Installation
============

::

    $ pip install urlwait

Usage
=====

::

    $ urlwait --help

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

The module is also usable in your python code::

    import os

    from urlwait import wait_for_url


    if wait_for_url(os.getenv('REDIS_URL')):
        # do things with the service
    else:
        # service likely did not start

If you don't have the service URL but do have the host and port, you can use the
``wait_for_service(host, port, timeout)`` function instead.


Python Support
==============

Since version 1.0 urlwait is Python 3 only. If you need Python 2.7 support you can use a pre 1.0 release.

Changelog
=========

* 1.0 - 2020-02-28
  * Close the socket to keep Python from complaining. Thanks @callahad!
  * Update tests to only test on Python 3.6+
  * Drop support for Python 2.x
* 0.4 - 2017-03-02 - Always return true if protocol is sqlite
