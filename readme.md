# Cocode
<small>Ver. Chaser</small>

This is a [Django](https://www.djangoproject.com/) & [Vue.js](https://vuejs.org/) based standalone web application that allows users to easily develop and share simple web applications.

## Setup

Make sure to have following requirements installed on your environment.
- [Python 3.5 or above](https://www.python.org/) 
- [Node 8 or above](https://nodejs.org/en/)
- [Yarn 1.0 or above](https://yarnpkg.com/en/)

### Dependencies

Python dependencies are managed by pip with [venv](https://docs.python.org/3/library/venv.html), and Node dependencies are managed by Yarn. 

It is recommended to use node scripts to manage all dependencies. In this case, your Python virtual environment will be created and maintained at `env` directory.

If you want to run `pip` or `python` in your virtual environment without activating the environment, simply run as yarn scripts as follows:

```bash
cocode $ yarn python
cocode $ yarn pip install django
```

### Development Server

To initialize and setup all dependencies, run the following command:

```bash
cocode $ yarn install
```

To run all development servers:

```bash
cocode $ yarn start
```

## Build

To build the application, run:

```bash
cocode $ yarn build
```

## Development

### Migrations

Working with migrations is simple. Make changes to your models - say, add a field and remove a model - and then run makemigrations:

```bash
cocode $ yarn manage makemigrations
Migrations for 'books':
  books/migrations/0003_auto.py:
    - Alter field author on book
```

Your models will be scanned and compared to the versions currently contained in your migration files, and then a new set of migrations will be written out. Make sure to read the output to see what makemigrations thinks you have changed - it’s not perfect, and for complex changes it might not be detecting what you expect.

Once you have your new migration files, you should apply them to your database to make sure they work as expected:

```bash
cocode $ yarn manage migrate
Operations to perform:
  Apply all migrations: books
Running migrations:
  Rendering model states... DONE
  Applying books.0003_auto... OK
```

Once the migration is applied, commit the migration and the models change to your version control system as a single commit - that way, when other developers (or your production servers) check out the code, they’ll get both the changes to your models and the accompanying migration at the same time.

## Deploy

Cocode supports a dockerized deployment. Simply use docker compose to deploy the project.

```bash
cocode $ docker-compose build
cocode $ docker-compose up
```

## Translate

Internationalization of this project is entirely based on Django's i18n feature. 

Use following command to make translation file:
```
cocode $ yarn makemessages
cocode $ yarn makemessages -l "en_US"
```

and use following command to compile translation file:

```
cocode $ yarn compilemessages
```

Make sure you have `gettext` installed and available in your `PATH`. 
Do not use `makemessages` or `compilemessages` directly with `django-admin` or 'manage.py` but use the yarn scripts above to avoid conflicts with Python venv or node modules. 