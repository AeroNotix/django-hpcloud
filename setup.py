from distutils.core import setup

setup(name='django_hpcloud',
      version='0.1',
      description='HPCloud module for Django',
      author='Aaron France',
      author_email='aaron.france@hp.com',
      url='http://github.com/AeroNotix/django-hpcloud',
      package_dir={
        'django_hpcloud': ''
        },
      packages=[
        'django_hpcloud',
        'django_hpcloud.templatetags',
        'django_hpcloud.management',
        'django_hpcloud.management.commands',
        ],
     )
