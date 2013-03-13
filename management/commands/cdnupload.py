import os, sys
from stat import *
import urllib2

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django_hpcloud.authentication import get_auth_token


class Command(BaseCommand):
    help = 'Uploads all static content into the HPCloud CDN'

    def handle(self, *args, **options):
        for directory in settings.STATICFILES_DIRS:
            process_directory(directory, directory)

def process_directory(basedir, top):
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname).st_mode
        if S_ISDIR(mode):
            create_directory(basedir, top, pathname)
            process_directory(basedir, pathname)
        elif S_ISREG(mode):
            upload_file(basedir, top, pathname)

def create_directory(basedir, top, pathname):
    if top[-1] != os.path.sep:
        top = top + os.path.sep
    baseprefix = len(os.path.commonprefix([basedir, top]))
    base = pathname[baseprefix:]
    path = "%s%s/%s" % (settings.OBJECT_STORE_URL, settings.TENANT_ID, base)
    req = urllib2.Request(path, '')
    req.add_header("Content-type", "application/directory")
    req.add_header("X-Auth-Token", get_auth_token())
    req.get_method = lambda: "PUT"
    res = urllib2.urlopen(req).read()
    if res or res == "":
        print "Created directory: %s" % base
    else:
        print res

def upload_file(basedir, top, pathname):
    if top[-1] != os.path.sep:
        top = top + os.path.sep
    baseprefix = len(os.path.commonprefix([basedir, top]))
    base = pathname[baseprefix:]
    path = "%s%s/%s" % (settings.OBJECT_STORE_URL, settings.TENANT_ID, base)
    req = urllib2.Request(path, open(pathname).read())
    req.add_header("X-Auth-Token", get_auth_token())
    req.get_method = lambda: "PUT"
    if urllib2.urlopen(req).read() == "":
        print "Uploaded: %s" % pathname
