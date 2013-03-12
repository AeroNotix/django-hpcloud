Django-hpcloud
==============


Django-hpcloud is a helper module intended for use with django to hook into the
HPCloud services.

You need to supply in your settings.py file:

* HP_SECRET_KEY
* HP_ACCESS_KEY
* HPCLOUD_USERNAME
* HPCLOUD_PASSWORD
* TENANT_ID
* OBJECT_STORE_URL
* REGION_URL


Where:

HP_SECRET_KEY
-------------

This can be found in the API Keys section in the console.

HP_ACCESS_KEY
-------------

This can be found in the API Keys section in the console.

HPCLOUD_USERNAME, HPCLOUD_PASSWORD and TENANT_ID
------------------------------------------------

You should know these yourself, if not you can head to hpcloud.com and ask for
a reminder.

OBJECT_STORE_URL
----------------

On your API Keys section page there will be an object store url. This is that
value.

REGION_URL
----------

Again, this is on your API Keys section page.
