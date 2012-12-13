.. -*- restructuredtext -*-

This is the code for Mark Liu's personal blog. You are free to use it or modify it however you please.


Local Installation
==================

This blog is just the glue that holds together several other more powerful django applications. I highly recommend using pip and virtualenv for doing so, so you do not run into any conflicts with other python applications you may be running now or in the future. 

I will assume you already have git installed and will not work you through that. Next, you need to have pip, and virtualenv installed. To do that, simply run::

    $ easy_install pip
    $ pip install virtualenv
    $ pip install virtualenvwrapper

Next, you need to create a virtualenvironment, and install this blog along with its dependencies. For that, you could do something like::
    
    $ mkvirtualenv myblog
    $ workon myblog

Now you're ready to clone this repo and get working::

    $ git clone https://github.com/mliu7/personal-django-blog.git
    $ cd personal-django-blog

Next, you need to install all of the dependencies::

    $ pip install -r requirements.txt

Next, you will need to download and update all of the git submodules::

    $ git submodule init
    $ git submodule update

Next, you need to update your python path so your system knows where to look for these submodules::

    $ add2virtualenv .
    $ cd markliu
    $ add2virtualenv .
    $ cd submodules
    $ add2virtualenv coltrane-blog
    $ add2virtualenv django-google-webmaster
    $ add2virtualenv django-posterous
    $ add2virtualenv django-twitter-tags

Next, configure your local settings by copying `local_settings.txt` to `local_settings.py` and filling in all of the necessary fields::

    $ cd ..
    $ cp local_settings.txt local_settings.py
    $ vi local_settings.py

Next, you'll need to create your database::

    $ createdb myblog_dev
    $ python manage.py syncdb
    $ python manage.py migrate

Once you've done that you can run your server::

    $ python manage.py runserver

If you navigate to ``http://127.0.0.1:8000/`` you should see the blog, and if you navigate to ``http://127.0.0.1:8000/admin`` you should be able to add some entries and links to the blog. 


Deploying to Heroku
===================

This part is surprisingly easy because Heroku is awesome. You can follow their instructions here: https://devcenter.heroku.com/articles/django#deploy-to-heroku

If you're too lazy to read that, just download the heroku toolbelt and do this::

    $ heroku create
    $ git push heroku master

You will now need to create the database on heroku::

    $ heroku run python markliu/manage.py syncdb
    $ heroku run python markliu/manage.pymigrate 

Next, you'll need to set your environment variables on Heroku as specified in this tutorial: https://devcenter.heroku.com/articles/config-vars ::

    $ heroku config:add AWS_STORAGE_BUCKET_NAME=mybucket
    $ heroku config:add AWS_SECRET_ACCESS_KEY=
    $ heroku config:add AWS_ACCESS_KEY_ID=
    $ heroku config:add GOOGLE_WEBMASTER_KEY=
    $ heroku config:add SECRET_KEY=
    $ heroku config:add DISQUS_API_KEY=
    $ heroku config:add DELICIOUS_PASSWORD=
    
I left the actual values off which you'll have to fill in of course. And finally, you'll have to update the python path to point to all of the submodules.::

    $ heroku config:add PYTHONPATH=/app:/app/markliu/:/app/markliu/templates/:/app/markliu/submodules/coltrane-blog/:/app/markliu/submodules/django-google-webmaster/:/app/markliu/submodules/django-posterous/:/app/markliu/submodules/django-twitter-tags/

That should be it! If you have any problems with any of these steps, Heroku's documentation is excellent and should help you resolve your issues.


Deploying your static resources to S3
=====================================

This repository is set up to work with Amazon S3. The way this works is you send your static resources to S3 when you are on your localhost and then when you are on production your site uses the S3 URL to fetch those static resources.

From your local environment, do the following::

    $ python manage.py collectstatic

Collectstatic will copy all of your files to the AWS and heroku will use the S3 URL you specified to 


Updating the database from Production
=====================================

Since this blog connects to Heroku, you should first download the datadump from heroku. Then run the following command::

    $ pg_restore -U username -d markliu_dev -O --clean latest.dump 
