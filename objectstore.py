import urllib2

from django.conf import settings
from django_hpcloud.authentication import get_auth_token


def create_directory(container):
    '''Creates a directory in the Object Store.

    :param container: :class:`str` The name of the directory to make.
    '''
    container = "%s%s/%s/%s?format=json" % (
        settings.OBJECT_STORE_URL, settings.TENANT_ID,
        settings.OBJECT_STORE_CONTAINER, container
    )
    req = urllib2.Request(container)
    req.add_header("Content-type", "application/directory")
    req.add_header("Content-length", "0")
    req.add_header("Accept", "application/json")
    req.add_header("X-Auth-Token", get_auth_token())
    req.get_method = lambda: "PUT"
    response = urllib2.urlopen(req)
    return response.getcode()
    
