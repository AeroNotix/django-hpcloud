import os, sys
import urllib2
import mimetypes; mimetypes.init()
from stat import *

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django_hpcloud.authentication import get_auth_token


class Command(BaseCommand):
    args = 'Name of base container to use'
    help = 'Uploads all static content into the HPCloud CDN'

    def handle(self, *args, **options):
        try:
            self.settings = settings.HPCLOUD_TTL_MAP
        except AttributeError:
            self.settings = {}
        if not args:
            self.stdout.write("A container name is required.\n")
            return
        self.container = args[0]
        # will create the base container
        self.create_directory(self.prepare_path(""))
        for directory in settings.STATICFILES_DIRS:
            self.basedir = directory
            self.process_directory(directory)

    def process_directory(self, top):
        '''
        process_directory will iterate recursively through an entire directory
        and create a container on the ObjectStore for each directory and upload
        files to the ObjectStore for each file.
        '''
        for f in os.listdir(top):
            pathname = os.path.join(top, f)
            mode = os.stat(pathname).st_mode
            if S_ISDIR(mode):
                self.create_subdirectory(top, pathname)
                self.process_directory(pathname)
            elif S_ISREG(mode):
                self.upload_file(top, pathname)

    def create_directory(self, pathname):
        req = urllib2.Request(pathname, '')
        req.add_header("Content-Type", "application/directory")
        req.add_header("X-Auth-Token", get_auth_token())
        req.get_method = lambda: "PUT"
        res = urllib2.urlopen(req).read()
        if res or res == "":
            self.stdout.write("Created directory: %s\n" % pathname)
        else:
            self.stdout.write("%s\n" % res)

    def create_subdirectory(self, top, pathname):
        '''
        create_directory will perform a PUT on the ObjectStore to create a directory
        with application/directory Content-type so that it will be created as
        an ObjectStore container.
        '''
        if top[-1] != os.path.sep:
            top = top + os.path.sep
        baseprefix = len(os.path.commonprefix([self.basedir, top]))
        base = pathname[baseprefix:]
        path = self.prepare_path(base)
        return self.create_directory(path)

    def upload_file(self, top, pathname):
        '''
        Uploads a file to the ObjectStore using the TTL value defined in the
        settings file and setting the correct mimetypes.
        '''
        # fix path ending to /
        if top[-1] != os.path.sep:
            top = top + os.path.sep
        baseprefix = len(os.path.commonprefix([self.basedir, top]))
        base = pathname[baseprefix:]
        path = self.prepare_path(base)
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

    def prepare_path(self, path):
        '''
        Prepares a path by interpolating all strings into a URL.
        '''
        return "%s%s/%s/%s" % (
            settings.OBJECT_STORE_URL, settings.TENANT_ID,
            self.container, path
            )
