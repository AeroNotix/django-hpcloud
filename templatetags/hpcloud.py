# Register this as a template tag library
from django import template
register = template.Library()

from django_hpcloud.cdn import CDN_ENABLED_CONTAINERS


class CDNUrl(template.Node):
    def __init__(self, container, path, protocol):
        self.container = container
        self.path = path
        self.protocol = protocol
    def render(self, context):
        return cdn(self.container, self.path, self.protocol)

def cdn(container, path, protocol):
    cdncontainer = CDN_ENABLED_CONTAINERS.get(container)
    if cdncontainer:
        return "%s/%s" % (cdncontainer[protocol], path)
    else:
        return ""

def parse_cdn(parser, token):
    tokens = token.split_contents()
    if len(tokens) == 3:
        return CDNUrl(tokens[1], tokens[2], "http")
    if len(tokens) == 4:
        return CDNUrl(tokens[1], tokens[2], tokens[3])

register.tag('cdn', parse_cdn)
