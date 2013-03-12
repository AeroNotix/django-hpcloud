import os, sys
from stat import *

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Uploads all static content into the HPCloud CDN'

    def handle(self, *args, **options):
        if not args:
            print "Container name required"
            return

        for directory in settings.STATICFILES_DIRS:
            print directory
            for f in list(walktree(directory)):
                print f

def walktree(top):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname).st_mode
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            print pathname
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname
