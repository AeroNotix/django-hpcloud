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
* CDN_URL
* HPCLOUD_TTL_MAP

Most of these can be found on your API Keys page. The HPCLOUD_TTL_MAP is a map
between extension types and their "Time To Live" in seconds, which, when uploaded
to the CDN is the number of seconds they will be cached for.

.. code-block:: python
    HPCLOUD_TTL_MAP = {
        ".css": "900",
        ".js": "1"
    }

This would make css files last for 900 seconds (15 minutes) in the cache and
Javascript files for only a second (which means they will never be cached.)

Using the django-hpcloud module.

The primary benefit so far is being able to transparently access your CDN containers
via template tags.

When the module is first loaded it queries the HPCloud endpoints for your CDN enabled
containers. You can then create templates such as:


.. code-block html

{% load hpcloud %}

<html>
  <body><h3>Awesome Gallery</h3>
  {% for pic in pictures %}
     <img href="{% cdn container pic.name %}" />
  {% endfor %}
  </body>
</html>
   
