from django.contrib.auth import views
from django.urls import include, path
from knox import views as knox_views
from rest_framework import routers
from rest_framework.authtoken import views as authviews

from knoxth.views import ContextViewSet, KnoxthLoginView

router = routers.DefaultRouter()
router.register(r'contexts', ContextViewSet)


app_name = 'knoxth'
urlpatterns = [
    path('authorize/', authviews.obtain_auth_token, name="knoxth_authorize"),
    path('login/', KnoxthLoginView.as_view(), name='knoxth_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knoxth_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),

    path('', include(router.urls)),
]
