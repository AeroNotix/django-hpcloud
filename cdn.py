import urllib2
import simplejson
import datetime

from django.conf import settings

from django_hpcloud.authentication import get_auth_token

def _get_cdn_enabled_containers():
    path = "%s%s?format=json" % (settings.CDN_URL, settings.TENANT_ID)
    req = urllib2.Request(path)
    req.add_header("Content-type", "application/json")
    req.add_header("X-Auth-Token", get_auth_token())
    response = urllib2.urlopen(req)
    enabled_containers = {}
    for container in simplejson.loads(response.read()):
        enabled_containers[container['name']] = {
            "https": container['x-cdn-ssl-uri'],
            "http":  container['x-cdn-uri']
            }
    return enabled_containers
CDN_ENABLED_CONTAINERS = _get_cdn_enabled_containers()
