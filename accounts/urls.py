from django.urls import path

from .viewsets import PublicUserViewSet, UserViewSet

urlpatterns = [
    path("register/", PublicUserViewSet.as_view({"post": "create_user"}), name="register"),
    path("login/", PublicUserViewSet.as_view({"post": "login"}), name="login"),
    path("user/", UserViewSet.as_view({"get": "get_user", "patch": "update_user"}), name="user"),
    path("logout/", UserViewSet.as_view({"post": "logout"}), name="logout"),
]
