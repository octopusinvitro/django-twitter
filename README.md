[![Python version](https://badgen.net/badge/python/3.10/yellow)](Pipfile)
[![License](https://img.shields.io/github/license/octopusinvitro/django-twitter)](https://github.com/octopusinvitro/django-twitter/blob/main/LICENSE.md)
[![Maintainability](https://api.codeclimate.com/v1/badges/aea7a26480b189eba0af/maintainability)](https://codeclimate.com/github/octopusinvitro/django-twitter/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/aea7a26480b189eba0af/test_coverage)](https://codeclimate.com/github/octopusinvitro/django-twitter/test_coverage)
[![Build status](https://gitlab.com/octopusinvitro/django-twitter/badges/main/pipeline.svg)](https://gitlab.com/octopusinvitro/django-twitter/commits/main)


# README

This is an attempt to build Twitter with Django.

It uses:
* `pipenv` for dependency management,
* PostgreSQL for storage,
* `unittest` as a testing framework,
* the `coverage` and `factory_boy` packages, and
* a custom `User` model.

It also allows to upload images. In development and production, they will be stored in `webapp/static/images/uploads`. In tests they will be stored in `tests/fixtures/uploads` and deleted afterwards.

You can edit users but you can not edit tweets.



## Setup

* The project uses translations, so make sure you have `gettext` in your system:

  ```sh
  sudo apt -y install gettext
  ```

* You will also need to install dependencies for [the python-to-PostgreSQL adapter](https://www.psycopg.org/docs/install.html):

  ```sh
  sudo apt update && sudo apt install python3-dev libpq-dev
  ```

* Create a user for the project in postgres, then create the database and assign it to this user:

  ```sh
  sudo -u postgres createuser --interactive
  sudo -u postgres psql
  >  ALTER ROLE user WITH PASSWORD 'password';
  >  CREATE DATABASE django_twitter OWNER user;
  ```

* Then update your user and password in `django_twitter/settings.py`. You may also have to update the host to localhost (`HOST': '127.0.0.1'`):

  ```python
  DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'django_twitter',
    'USER': 'postgres',  # UPDATE THIS
    'PASSWORD': '',      # UPDATE THIS
    'HOST': 'postgres', # UPDATE THIS
    'PORT': '5432'
  }
  ```

  The test database will be created automatically by Django.


## Install

Once you have done the setup in the previous section, you can install the project dependencies, run the migrations and create a superuser for the admin panel:

```sh
pipenv install
. bin/migrate
pipenv run ./manage.py createsuperuser
```

If you don't want to manually seed your database for development, you can use the provided fixture:
```sh
pipenv run ./manage.py loaddata webapp.json
```

## To run

```sh
. bin/run
```

Then go to <http:localhost:8000>.

### Migrations

To create new migrations and run them:

```sh
. bin/migrate
```

To check what the migration would do:

```sh
pipenv run ./manage.py sqlmigrate webapp 0001
```

## To test

Run all the tests and open a coverage report in Firefox:
```sh
. bin/test
```

Run all the tests in a file:
```sh
. bin/test tests.path.to.file
```

Run just one test method:
```sh
. bin/test tests.path.to.file.YourTestClassName.test_method_name
```


## To lint

```sh
. bin/lint
```


# To debug

Throw an `import pdb; pdb.set_trace()` in the part of the code where you want to start debugging, and run the tests.

# To do

* [ ] [Security checklist](https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/)
* [ ] Mock `SimpleUploadedFile` and simplify tweets view tests.
* [ ] Image uploader is a button and you can preview the image rather than the filename (https://www.section.io/engineering-education/an-extensive-guide-on-handling-images-in-django/)
* [ ] Send a list of tweet presenters instead of a list of tweets
* [ ] Sort tweets by date before display
* [ ] Write down how to dump and load data to the db in the README
* [ ] Write about image upload and custom user in my blog
* [ ] Add email validation
* [ ] Delete the import of the tweet model in __init__
* [ ] `from django.contrib.auth import get_user_model cls.User = get_user_model()`
* [ ] [Delete files when deleting models](https://cmljnelson.blog/2020/06/22/delete-files-when-deleting-models-in-django/)
* [ ] resize and compress image, set max size and weight, show constrains in form [startt here maybe](https://odwyer.software/blog/how-to-validate-django-imagefield-dimensions)

```sh
rm webapp/tests/fixtures/uploads/attachments/* webapp/tests/fixtures/uploads/avatars/*
pipenv run ./manage.py dumpdata webapp > webapp.json
pipenv run ./manage.py dumpdata webapp.tweet > tweets.json

rm webapp/migrations/*
sudo -u postgres psql

drop database django_twitter;
drop database django_twitter_test;
create database django_twitter owner ubuntu;

. bin/migrate

pipenv run ./manage.py createsuperuser --username=ubuntu --email=ubuntu@example.com --display_name=Ubuntu

pipenv run ./manage.py loaddata tweets.json
```
