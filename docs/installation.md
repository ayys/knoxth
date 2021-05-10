# Installation

Knox should be installed with pip


## 1. Install knoxth
```bash
pip install knoxth
```

For pipenv projects, it can also be installed as such
```bash
pipenv install knoxth
```


After installing knoxth, you will need to setup knoxth to work with your existing project.
Before seting up knoxth, make sure you have rest_framework and knox setup and ready to go.

## 2. Add to INSTALLED_APPS

Add `rest_framework`, `knox` and `knoxth` to your `INSTALLED_APPS`, and add
`rest_framework.authtoken` if you removed it while setting up knox.

```python
INSTALLED_APPS = (
  ...
  'rest_framework',
  'rest_framework.authtoken',
  'knox',
  'knoxth',
  ...
)
```

## 3. Setup default Authentication class

Make knox's TokenAuthentication your default authentication class
for django-rest-framework:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    ...
}
```

## 4. Include knoxth URLS
Knoxth provides a url config ready with its four default views routed.

This can easily be included in your url config:

```python
urlpatterns = [
  #...snip...
  url(r'api/auth/', include('knoxth.urls'))
  #...snip...
]
```
**Note** It is important to use the string syntax and not try to import `knoxth.urls`,
as the reference to the `User` model will cause the app to fail at import time.

The views would then acessible as:

| Endpoint              | Description                                                         |
| ---                   | ---                                                                 |
| `/api/auth/authorize` | Authorize username & password. Return authorization code.           |
| `/api/auth/login`     | Accept authorization code and return access token                   |
| `/api/auth/logout`    | Logout the user and delete the access token and authorization code. |
| `/api/auth/logoutall` | Same as logout, but logs out of all running sessions.               |
|                       |                                                                     |

they can also be looked up by name:

```python
reverse('knoxth_login')
reverse('knoxth_logout')
reverse('knoxth_logoutall')
reverse('knoxth_authorize')
```


## 5. Migrate

Apply the migrations for the models

```bash
python manage.py migrate
```
