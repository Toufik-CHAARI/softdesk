from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentication.views import userViewset

router = DefaultRouter()
router.register(r"api-auth", userViewset, basename="user")


urlpatterns = [
    path("", include(router.urls)),
]
