import os

import pytest
from mock import patch

import urlwait


def test_service_class():
    service = urlwait.ServiceURL('redis://db/0')
    assert service.host == 'db'
    assert service.port == urlwait.DEFAUTL_PORTS['redis']

    service = urlwait.ServiceURL('redis://user:pass@localhost:8080/0')
    assert service.host == 'localhost'
    assert service.scheme == 'redis'
    assert service.port == 8080


@patch.object(urlwait, 'ServiceURL')
def test_wait_for_url(service_mock):
    url = 'mysql://root@the.dude/walter'
    urlwait.wait_for_url(url)
    service_mock.assert_called_with(url, urlwait.DEFAULT_TIMEOUT)


def test_wait_for_url_no_port():
    with pytest.raises(RuntimeError):
        urlwait.wait_for_url('thedude://maude@lebowski/bunny')


@patch.object(urlwait, 'ServiceURL')
def test_wait_for_service(service_mock):
    urlwait.wait_for_service('dude', 5000, 20)
    service_mock.assert_called_with('tcp://dude:5000', 20)


@patch.object(urlwait, 'ServiceURL')
def test_main(service_mock):
    os.environ['DATABASE_URL'] = 'mysql://root@db/logjammin'
    os.environ['CACHE_URL'] = 'redis://localhost/1'
    urlwait.main(['pgsql://db/postgres', '2'])
    service_mock.assert_called_with('pgsql://db/postgres', '2')

    urlwait.main()
    service_mock.assert_called_with('mysql://root@db/logjammin', urlwait.DEFAULT_TIMEOUT)

    os.environ['URLWAIT_VARNAME'] = 'CACHE_URL'
    os.environ['URLWAIT_TIMEOUT'] = '60'
    urlwait.main()
    service_mock.assert_called_with('redis://localhost/1', '60')
