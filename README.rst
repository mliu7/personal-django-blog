.. -*- restructuredtext -*-

This is the code for Mark Liu's personal blog. You are free to use it or modify it however you please.

Local Installation
==================

This blog is just the glue that holds together several other more powerful django applications. You will need to install these other applications for the blog to work. I highly recommend using pip and virtualenv for doing so, so you do not run into any conflicts with other python applications you may be running now or in the future. 

I will assume you already have git installed and will not work you through that. Next, you need to have pip, and virtualenv installed. To do that, simply run::

    $ easy_install pip
    $ pip install virtualenv
    $ pip install virtualenvwrapper

Next, you need to create a virtualenvironment, and install this blog along with its dependencies. For that, you could do something like::
    
    $ mkdir myblog
    $ cd myblog
    $ mkvirtualenv myblog
    $ workon myblog

Next, you need to have Django installed::
    
    $ pip install django

Now we need to copy all the code I wrote into your local directory::

    $ git clone -q git@github.com:mliu7/personal-django-blog.git    
    $ git clone -q git@github.com:mliu7/django-twitter-tags.git
    $ git clone -q git@github.com:mliu7/django-google-webmaster.git
    $ git clone -q git@github.com:mliu7/coltrane-blog.git

All of this code is now copied locally, but we need to make sure it is all on our virtual environment's python path. To do that, we can just type the following::

    $ add2virtualenv django-twitter-tags
    $ add2virtualenv django-google-webmaster
    $ add2virtualenv coltrane-blog

Next, we need to install some django apps this code is dependent on::

    $ cd personal-django-blog
    $ pip install distribute
    $ pip install -r requirements.txt

Finally, you need to add a ``settings.py`` file in the ``myblog/personal-django-blog/markliu`` folder. There is a sample settings file called ``sample_settings.py`` that you can modify to your liking. Django has great documentation for you to set up one of these on your own. 

Once your settings file is complete and you have set up all your database preferences, you can create the database by running django's built in ``syncdb`` command followed by some built in south commands. Before you can do this, though, you'll want to comment out the coltrane app declaration in your ``settings.py`` file so we can create a fresh south installation of this app. In other words, comment this line in your ``settings.py`` file::

    INSTALLED_APPS = (
        ... 
        #'coltrane',
        ...
    )

Once this is commented out, you can create all of the database tables for your app except for the coltrane tables by running::

    $ python manage.py syncdb

After these tables are created and you set up your superuser account which it asks you to do automatically, jump back into your ``settings.py`` file and uncomment that line::

    INSTALLED_APPS = (
        ... 
        'coltrane',
        ...
    )

Close ``settings.py`` and create your first south migration for the coltrane app::

    $ python manage.py schemamigration coltrane --init
    $ python manage.py migrate coltrane

Now that you've done this, you can start your webserver and it should work! Just run the following::
    
    $ python manage.py runserver

If you navigate to ``http://127.0.0.1:8000/`` you should see the blog, and if you navigate to ``http://127.0.0.1:8000/admin`` you should be able to add some entries and links to the blog. 

Good luck, and I hope this helps some people out there!
