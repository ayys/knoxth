"""
There are a total of four rest endpoints exposed by knxoth,
which you may use to implement auth-code based authorization
for your app.

LOGIN FLOW:

POST authorize/ with username and password in body
POST login/ with the auth-code from previus step


LOGOUT FLOW:
GET logout/

LOGOUT FROM ALL DEVICES:
GET logoutall/
"""

from django.urls import include, path
from knox import views as knox_views
from rest_framework import routers
from rest_framework.authtoken import views as authviews

from knoxth.views import (
    AuthTokenViewset,
    ContextViewSet,
    KnoxthLoginView,
    LogoutAllExceptCurrentView,
)

router = routers.DefaultRouter()
router.register(r"contexts", ContextViewSet)
router.register(r"tokens", AuthTokenViewset, basename="tokens")


app_name = "knoxth"
urlpatterns = [
    path("authorize/", authviews.obtain_auth_token, name="knoxth_authorize"),
    path("login/", KnoxthLoginView.as_view(), name="knoxth_login"),
    path("logout/", knox_views.LogoutView.as_view(), name="knoxth_logout"),
    path("logout-all/", knox_views.LogoutAllView.as_view(), name="knoxth_logoutall"),
    path(
        "logout-all-except-current/",
        LogoutAllExceptCurrentView.as_view(),
        name="knoxth_logout_all_except_current",
    ),
    path("", include(router.urls)),
]
