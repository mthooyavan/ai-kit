.. _installation:

Installation
============

AiKit is easy to install from the PyPI package::

    $ pip install django-ai-kit

After installing the package, the project settings need to be configured.

**1.** Add ``ai_kit`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # AiKit app can be in any position in the INSTALLED_APPS list.
        'ai_kit',
    ]

**4.** Run ``python manage.py check`` to check the configuration.

**5.** Run ``python manage.py migrate`` to sync the database.

AiKit is now functional with the default settings and is saving user attempts
into your database and locking users out if they exceed the maximum attempts.

You should use the ``python manage.py check`` command to verify the correct configuration in
development, staging, and production environments. It is probably best to use this step as part
of your regular CI workflows to verify that your project is not misconfigured.
