from django.urls import include, path
from knox import views as knox_views
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"api/users", views.UserViewSet)
router.register(r"api/groups", views.GroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api/login/", views.LoginAPI.as_view(), name="login"),
    path("api/logout/", knox_views.LogoutView.as_view(), name="logout"),
    path("api/logoutall/", knox_views.LogoutAllView.as_view(), name="logoutall"),
    path("api/register/", views.RegisterAPI.as_view(), name="register"),
    path("api/products/", include("products.urls")),
]
