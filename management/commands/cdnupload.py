import os, sys
import urllib2
import mimetypes; mimetypes.init()
from stat import *

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django_hpcloud.authentication import get_auth_token


class Command(BaseCommand):
    help = 'Uploads all static content into the HPCloud CDN'

    def handle(self, *args, **options):
        try:
            self.settings = settings.HPCLOUD_TTL_MAP
        except AttributeError:
            self.settings = {}

        for directory in settings.STATICFILES_DIRS:
            self.basedir = directory
            self.process_directory(directory)

    def process_directory(self, top):
        for f in os.listdir(top):
            pathname = os.path.join(top, f)
            mode = os.stat(pathname).st_mode
            if S_ISDIR(mode):
                self.create_directory(top, pathname)
                self.process_directory(pathname)
            elif S_ISREG(mode):
                self.upload_file(top, pathname)

    def create_directory(self, top, pathname):
        if top[-1] != os.path.sep:
            top = top + os.path.sep
        baseprefix = len(os.path.commonprefix([self.basedir, top]))
        base = pathname[baseprefix:]
        path = "%s%s/%s" % (settings.OBJECT_STORE_URL, settings.TENANT_ID, base)
        req = urllib2.Request(path, '')
        req.add_header("Content-Type", "application/directory")
        req.add_header("X-Auth-Token", get_auth_token())
        req.get_method = lambda: "PUT"
        res = urllib2.urlopen(req).read()
        if res or res == "":
            print "Created directory: %s" % base
        else:
            print res

    def upload_file(self, top, pathname):
        if top[-1] != os.path.sep:
            top = top + os.path.sep
        baseprefix = len(os.path.commonprefix([self.basedir, top]))
        base = pathname[baseprefix:]
        path = "%s%s/%s" % (settings.OBJECT_STORE_URL, settings.TENANT_ID, base)
        req = urllib2.Request(path, open(pathname).read())
        ext = os.path.splitext(path)[1]
        mimetype = mimetypes.types_map.get(ext)
        if mimetype:
            req.add_header("Content-Type", mimetype)
        # default 24 hours
        req.add_header("X-TTL", self.settings.get(ext, "86400"))
        req.add_header("X-Auth-Token", get_auth_token())
        req.get_method = lambda: "PUT"
        if urllib2.urlopen(req).read() == "":
            print "Uploaded: %s" % pathname
