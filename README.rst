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


.. code-block:: html

    {% load hpcloud %}

    <html>
      <body><h3>Awesome Gallery</h3>
      {% for pic in pictures %}
         <img href="{% cdn container pic.name %}" />
      {% endfor %}
      </body>
    </html>


Also, from the command line this module provides a django command which helps
you upload all your static files into the object store.

.. code-block:: bash

   $ python manage.py cdnupload
    Created directory: css
    Uploaded: /var/www/project/static/css/bootstrap.css
    Uploaded: /var/www/project/static/css/bootstrap-responsive.min.css
    Uploaded: /var/www/project/static/css/bootstrap.min.css
    Uploaded: /var/www/project/static/css/bootstrap-responsive.css
    Created directory: img
    Uploaded: /var/www/project/static/img/glyphicons-halflings.png
    Uploaded: /var/www/project/static/img/glyphicons-halflings-white.png
    Created directory: js
    Uploaded: /var/www/project/static/js/bootstrap.js
    Uploaded: /var/www/project/static/js/bootstrap.min.js
