======
Pipeye
======


Running the app
===============

Both ``manage.py`` and ``wsgi.py`` were modified not to let you run app
without choosing one of the settings files. There are three available ones:

``pipeye.settings.prod``
    For production use. Requires settings following environmental variables:

    - DATABASE_URL
    - SECRET_KEY
    - GITHUB_APP_ID
    - GITHUB_API_SECRET

``pipeye.settings.dev``
    For local development. Will use postgres database named pipeye. Requires
    setting github credentials environmental variables.

``pipeye.settings.test``
    For speed testing. Will use sqlite in-memory database and has downgraded
    password hashes.


Running tests
-------------

To run tests under postgres::

    $ ./manage.py test --settings=pipeye.settings.dev

To run tests under sqlite in-memory storage::

    $ ./manage.py test --settings=pipeye.settings.test


Development tip
---------------

Put this in your ``$VIRTUAL_ENV/bin/postactivate`` to ease the pain of
development::

    # Enter project directory
    cd ~/path/to/pipeye

    # Use dev settings by default
    export DJANGO_SETTINGS_MODULE=pipeye.settings.dev

    # Use your GitHub app id and secret
    export GITHUB_APP_ID=<app_id>
    export GITHUB_API_SECRET=<api_secret>
