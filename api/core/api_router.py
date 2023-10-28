from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from api.users.views import UserViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# USERS
router.register("users", UserViewSet)

app_name = "v1"
urlpatterns = router.urls
urlpatterns += [
    path("polls/", include("api.polls.urls"), name="polls"),
    path("channels/", include("api.channels.urls"), name="channels")
]