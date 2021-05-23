<h1 align="center">
  <br>
  <img src="https://raw.githubusercontent.com/ayys/knoxth/master/images/logo.svg" width="200" />
  <br>
  Knoxth - Auth for Knox
  <br>
</h1>

<h4 align="center">A authorization module for django built on top of <a href="django-rest-framework.org/" target="_blank">DRF</a> and <a href="https://james1345.github.io/django-rest-knox/" target="_blank">Knox</a>.</h4>

<p align="center">
  <a href="https://saythanks.io/to/ayushjha@pm.me"><img src="https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg"/></a>
 <a href="https://gitlab.com/ayys/knoxth/-/commits/master"><img alt="pipeline status" src="https://gitlab.com/ayys/knoxth/badges/master/pipeline.svg" /></a>
   <a href="https://github.com/ayys/knoxth/blob/master/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/ayys/knoxth"></a>
 <a href="https://gitlab.com/ayys/knoxth/-/commits/master"><img alt="coverage report" src="https://gitlab.com/ayys/knoxth/badges/master/coverage.svg" /></a>
</p>

<p align="center">
<a href="#introduction">Introduction</a> •
  <a href="#installation">Installation</a> •
  <a href="https://ayys.gitlab.io/knoxth/getting-started/">How To Use</a> •
  <a href="https://ayys.gitlab.io/knoxth/">Documentation</a> •
  <a href="#license">License</a>
</p>

## Introduction

Knoxth uses Knox tokens to provide token-level authorization management for DRF viewsets.

Django Rest Frameowork is an amazingly simple to use and easy
frameowork to write REST APIs in Django. With Knox, you can secure
your API with Access Tokens. Yet, there is a gap left by Knox, the
need for context-specific authentication system built on top of knox.

Users will want to customize the "scope" of each token they
create. This way, users may create different tokens for separate
usecases.

Let's take an example. Let us say you are developinga rest api that
lets it's create and manage TODO lists. Now, you have a viewset that
handles all CRUD operations, but you want to provide a way for users
to manage access to their todo lists on a token level. So, a user may
want to create a token, with which they can only read TODO lists, but
not modify them.

This is where knoxth comes in. Knoxth implements contextual
authorization of DRF viewsets on token level, using Knox Tokens.

## Installation

Knox should be installed with pip


### 1. Install knoxth
```bash
pip install knoxth
```

For pipenv projects, it can also be installed as such
```bash
pipenv install knoxth
```


After installing knoxth, you will need to setup knoxth to work with your existing project.
Before seting up knoxth, make sure you have rest_framework and knox setup and ready to go.

### 2. Add to INSTALLED_APPS

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

### 3. Setup default Authentication class

Make knox's TokenAuthentication your default authentication class
for django-rest-framework:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    ...
}
```

### 4. Include knoxth URLS
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


### 5. Migrate

Apply the migrations for the models

```bash
python manage.py migrate
```



## How To Use

Refer to our [documentation](https://ayys.gitlab.io/knoxth/") for details, or follow our [getting started guide](https://ayys.gitlab.io/knoxth/getting-started/").



## License

GNU GPL V3

---

> GitHub [@ayys](https://github.com/ayys) &nbsp;&middot;&nbsp;
> Twitter [@habuayush](https://twitter.com/habuayush)
