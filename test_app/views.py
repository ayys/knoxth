from django.contrib.auth import get_user_model
from rest_framework import viewsets

from knoxth.decorators import withContext
from test_app.serializers import UserSerializer

User = get_user_model()


# Create your views here.
@withContext(context="users")
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
