import urllib2
import simplejson
import datetime

from django.conf import settings

def get_object_list(container):
    container = "%s%s/%s" % (settings.OBJECT_STORE_URL, settings.TENANT_ID, container)
    print container
    req = urllib2.Request(container)
    req.add_header("Content-type", "application/json")
    req.add_header("X-Auth-Token", get_auth_token())
    response = urllib2.urlopen(req)
    return response.read().split('\n')


def _get_cdn_enabled_containers():
    path = "%s%s" % (settings.CDN_URL, settings.TENANT_ID)
    return path
CDN_ENABLED_CONTAINERS = _get_cdn_enabled_containers()
    
