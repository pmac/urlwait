=======
URLWait
=======

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