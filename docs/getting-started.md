# Quickstart

We are going to create a simple Django API called `petlovers` with
two views - A `cat view` and a `dog view`. Users who register to the
website can either be a `dog lover` or a `cat lover`. The dog lovers
and cat lovers can only view the `dog view` and `cat view`
respectively.

![Overall view of the cat-dog app][cat-dog-overall]

## 1. Project setup

Create a new Django project named `petlovers`, then create an app
called `pets`.

    # Setup a pipenv virtual environment with necessary dependencies
    pipenv install django djangorestframework django-rest-knox knoxth

    # Set up a new project with a single application
    pipenv run django-admin startproject petlovers
    cd petlovers
    pipenv run django-admin startapp pets


The project layout should look like:

    $ pwd
    <some path>/petlovers
    $ find .
    .
    ./petlovers
    ./petlovers/pets
    ./petlovers/pets/migrations
    ./petlovers/pets/migrations/__init__.py
    ./petlovers/pets/tests.py
    ./petlovers/pets/models.py
    ./petlovers/pets/apps.py
    ./petlovers/pets/views.py
    ./petlovers/pets/admin.py
    ./petlovers/pets/__init__.py
    ./petlovers/asgi.py
    ./petlovers/settings.py
    ./petlovers/urls.py
    ./petlovers/__init__.py
    ./petlovers/wsgi.py
    ./manage.py
    ./Pipfile.lock
    ./Pipfile

It may look unusual that the application has been created within the project directory. Using the project's namespace avoids name clashes with external modules (a topic that goes outside the scope of the quickstart).

### Add to INSTALLED_APPS

Add `rest_framework`, `knox` and `knoxth` to your `INSTALLED_APPS`, and add
`rest_framework.authtoken` if you removed it while setting up knox.

`petlovers/settings.py`
```python
INSTALLED_APPS = (
  ...
  'pets',
  'rest_framework',
  'rest_framework.authtoken',
  'knox',
  'knoxth',
  ...
)
```

### Setup default Authentication class

Copy this at the end of your `settings.py` to make knox's
TokenAuthentication your default authentication class
for django-rest-framework:

`petlovers/settings.py`
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    ...
}
```


Now sync your database for the first time:

    pipenv run ./manage.py migrate

We'll also create an initial user named `admin` with a password of
`password123`. We'll authenticate as that user later in our example.

    pipenv run ./manage.py createsuperuser --email admin@example.com --username admin

Once you've set up a database and the initial user is created and
ready to go, open up the app's directory and we'll get coding...

## 2. Create Models

First up we're going to define some models. We will be deffining two
models, `Cat` and `Dog`.

`pets/models.py`
```python
from django.db import models

# Create your models here.

class Pet(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()

    class Meta:
        abstract = True


class Cat(Pet):
    is_evil = models.BooleanField()


class Dog(Pet):
    barks_alot = models.BooleanField()
```

Notice that we are using an abstract model to store the common properties. Read more about them [over at the django docs](https://docs.djangoproject.com/en/3.2/topics/db/models/#abstract-base-classes).


## 3. Create Serializers
Serializers help us control data-accessability from our models to our views. For this tutorial, we will create a simple serializer for both the `Cat` and `Dog` modls.

Create a `serializers.py` in your `pets` app, with the following content.

`pets/serializers.py`
```python
'''
Serializers for pets models
'''

from rest_framework.serializers import ModelSerializer, ReadOnlyField

from pets.models import Cat, Dog


class CatSerializer(ModelSerializer):
    class Meta:
        model = Cat
        fields = ['name', 'age', 'is_evil']


class DogSerialiizer(ModelSerializer):
    class Meta:
        model = Dog
        fields = ['name', 'age', 'barks_alot']
```

## 4. Create views
Right, we'd better write some views then.  Open `pets/views.py` and get typing.

`pets/views.py`

```python
# Create your views here.
from django.shortcuts import render
from rest_framework import permissions, viewsets

from pets.models import Cat, Dog
from pets.serializers import CatSerializer, DogSerialiizer


class CatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cats to be viewed or edited.
    """
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [permissions.IsAuthenticated]


class DogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows dogs to be viewed or edited.
    """
    queryset = Dog.objects.all()
    serializer_class = DogSerialiizer
    permission_classes = [permissions.IsAuthenticated]

```
Rather than write multiple views we're grouping together all the common behavior into classes called `ViewSets`.

We can easily break these down into individual views if we need to, but using viewsets keeps the view logic nicely organized as well as being very concise.

## 5. Setup URLs
Okay, now let's wire up the API URLs.  On to `petlovers/urls.py`


`petlovers/urls.py`
```python
from django.urls import include, path
from pets.views import CatViewSet, DogViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'cats', CatViewSet)
router.register(r'dogs', DogViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('atuh/', include('knoxth.urls'))
]
```
Because we're using viewsets instead of views, we can automatically generate the URL conf for our API, by simply registering the viewsets with a router class.

Again, if we need more control over the API URLs we can simply drop down to using regular class-based views, and writing the URL conf explicitly.


## 5. The App So far

Right! So let's take a break and check if everything is in order. So far, we have created models, serializes and views. We also modified the settings.py with necessary configs.

So, lets migrate the changes and start the server.

```bash
pipenv run ./manage.py makemigrations
pipenv run ./manage.py migrate
pipenv run ./manage.py runserver
```

Make sure the server starts properly!

## 6. Setup users

## 7. Setup auth with knoxth


---

## 8. Testing our API

We're now ready to test the API we've built.  Let's fire up the server from the command line.

    python manage.py runserver

We can now access our API, both from the command-line, using tools like `curl`...

    bash: curl -H 'Accept: application/json; indent=4' -u admin:password123 http://127.0.0.1:8000/users/
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "email": "admin@example.com",
                "groups": [],
                "url": "http://127.0.0.1:8000/users/1/",
                "username": "admin"
            },
            {
                "email": "tom@example.com",
                "groups": [],
                "url": "http://127.0.0.1:8000/users/2/",
                "username": "tom"
            }
        ]
    }

Or using the [httpie][httpie], command line tool...

    bash: http -a admin:password123 http://127.0.0.1:8000/users/

    HTTP/1.1 200 OK
    ...
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "email": "admin@example.com",
                "groups": [],
                "url": "http://localhost:8000/users/1/",
                "username": "paul"
            },
            {
                "email": "tom@example.com",
                "groups": [],
                "url": "http://127.0.0.1:8000/users/2/",
                "username": "tom"
            }
        ]
    }


Or directly through the browser, by going to the URL `http://127.0.0.1:8000/users/`...

![Quick start image][image]

If you're working through the browser, make sure to login using the control in the top right corner.

Great, that was easy!

If you want to get a more in depth understanding of how REST framework fits together head on over to [the tutorial][tutorial], or start browsing the [API guide][guide].

[cat-dog-overall]: ./cat-dog-endpoint.png
[httpie]: https://github.com/jakubroztocil/httpie#installation
