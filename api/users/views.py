from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, generics
from rest_framework import mixins, status

from api.users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

