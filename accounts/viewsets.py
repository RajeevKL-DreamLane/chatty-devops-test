from rest_framework import viewsets
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class PublicUserViewSet(viewsets.ViewSet):
    permission_classes = ()
    authentication_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create_user(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = self.queryset.filter(username=username).first()
        if not user or not user.check_password(password):
            return Response({"error": "Invalid username or password"}, status=HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_user(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=HTTP_200_OK)

    def update_user(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)
