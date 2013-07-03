import hmac
from hashlib import sha1
from time import time
import urllib2
import simplejson

from django.conf import settings
from django_hpcloud.models import AuthToken

def generate_form_post_key(path, redirect,
                           expires=2147483647,
                           max_file_size=1073741824,
                           method='POST'):
    '''
    Generates the key for the FormPOST signatures. This is used for the file
    upload forms.

    :param path: :class:`str` The path of the directory to upload to, this should
                              not include the name of the file you're uploading.
    :param expires: :class:`int` The Unix timestamp of the expiry date of the form.
    :param max_file_size: :class:`int` The maximum file size of the files allowed
                                       to be uploaded with this form.
    :param method: :class:`str` The method which the form will be using, defaults to
                                POST because that's all that's supported but allows
                                others just in case.
    '''
    path = "/v1/%s/%s/" % (settings.TENANT_ID, path)
    hmac_body = "%s\n%s\n%s\n%s\n%s" % (
        path, redirect, max_file_size, "10", expires,
        )
    return "%s:%s:%s" % (
        settings.TENANT_ID, settings.HP_ACCESS_KEY,
        hmac.new(settings.HP_SECRET_KEY, hmac_body, sha1).hexdigest()
        )

def generate_share_url(path, expires=2147483647):
    '''
    Generates the URL for which you can create a time-sensitive link to any item
    in your object store.

    :param expires: :class:`int` The Unix timestamp of the expiry date of the form.
    '''
    hmac_path = "/v1/%s/%s" % (settings.TENANT_ID, path)
    hmac_body = "%s\n%s\n%s" % ("GET",expires, hmac_path)
    hmac_code = "%s:%s:%s" % (
        settings.TENANT_ID, settings.HP_ACCESS_KEY,
        hmac.new(settings.HP_SECRET_KEY, hmac_body, sha1).hexdigest()
        )
    path = "%s%s/%s?temp_url_sig=%s&temp_url_expires=%s" % (
        settings.OBJECT_STORE_URL, settings.TENANT_ID, path,
        hmac_code, expires)
    return path

def get_object_list(container):
    '''Returns a list of objects inside a container.

    :param container: :class:`str` The name of the container to list.
    '''
    container = "%s%s/%s?format=json" % (settings.OBJECT_STORE_URL, settings.TENANT_ID, container)
    req = urllib2.Request(container)
    req.add_header("Content-type", "application/json")
    req.add_header("X-Auth-Token", get_auth_token())
    response = urllib2.urlopen(req)
    return simplejson.loads(response.read())

def get_auth_token():
    '''Returns the auth_token currently being used.

    If the auth_token has expired, it will generate a new one and return that.
    '''
    if AuthToken.objects.all().count() > 0:
        token = AuthToken.objects.all()[0]
        if token.is_valid():
            return token.token
    AuthToken.objects.all().delete()
    json_data = {
        "auth": {
            "passwordCredentials": {
                "username": settings.HPCLOUD_USERNAME,
                "password": settings.HPCLOUD_PASSWORD
                },
            "tenantId": settings.TENANT_ID
            }
        }
    payload = simplejson.dumps(json_data)
    req = urllib2.Request(
        settings.REGION_URL + "tokens",
        )
    req.add_header("Content-type", "application/json")
    json = simplejson.loads(urllib2.urlopen(req, payload).read())
    AuthToken(token=json['access']['token']['id'],
              expires=json['access']['token']['expires']).save()
    return json['access']['token']['id']
