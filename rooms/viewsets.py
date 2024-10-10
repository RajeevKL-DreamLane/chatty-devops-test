from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer, ListRoomSerializer
from rest_framework.pagination import PageNumberPagination


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class AdminRoomViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdmin)
    queryset = Room.objects.all()
    serrializer_class = RoomSerializer

    def create_room(self, request):
        data = request.data
        data.update({"created_by": request.user.pk})
        serializer = RoomSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def add_member(self, request, pk):
        room = self.queryset.filter(pk=pk).first()
        if not room:
            return Response({"error": "Topic not found"}, status=HTTP_400_BAD_REQUEST)
        user = request.data.get("member")
        user = User.objects.filter(username=user).first()
        if not user:
            return Response({"error": "User not found"}, status=HTTP_400_BAD_REQUEST)
        room.members.add(user)
        return Response(status=HTTP_200_OK)

    def remove_member(self, request, pk):
        room = self.queryset.filter(pk=pk).first()
        if not room:
            return Response({"error": "Topic not found"}, status=HTTP_400_BAD_REQUEST)
        user = request.data.get("member")
        user = User.objects.filter(username=user).first()
        if not user:
            return Response({"error": "User not found"}, status=HTTP_400_BAD_REQUEST)
        room.members.remove(user)
        return Response(status=HTTP_200_OK)

    def delete_room(self, request, pk):
        room = self.queryset.filter(pk=pk).first()
        if not room:
            return Response({"error": "Topic not found"}, status=HTTP_400_BAD_REQUEST)
        room.delete()
        return Response(status=HTTP_200_OK)


class UserRoomViewSet(viewsets.ViewSet, ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        self.serializer_class = ListRoomSerializer
        return super().list(request, *args, **kwargs)

    def retrieve_room(self, request, pk):
        room = self.queryset.filter(pk=pk).first()
        if not room:
            return Response({"error": "Topic not found"}, status=HTTP_400_BAD_REQUEST)
        return Response(self.serializer_class(room).data, status=HTTP_200_OK)

    def subscribe_topic(self, request, pk):
        room = self.queryset.filter(pk=pk).first()
        if not room:
            return Response({"error": "Topic not found"}, status=HTTP_400_BAD_REQUEST)
        user = request.user
        room.members.add(user)
        return Response(status=HTTP_200_OK)

    def unsubscribe_topic(self, request, pk):
        room = self.queryset.filter(pk=pk).first()
        if not room:
            return Response({"error": "Topic not found"}, status=HTTP_400_BAD_REQUEST)
        user = request.user
        room.members.remove(user)
        return Response(status=HTTP_200_OK)


class MessageViewSet(viewsets.ViewSet, ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = PageNumberPagination

    def list(self, request, pk, *args, **kwargs):
        room = Room.objects.filter(pk=pk).first()
        if not room:
            return Response({"error": "Topic not found"}, status=HTTP_400_BAD_REQUEST)
        if not room.members.filter(pk=request.user.pk).exists():
            return Response({"error": "Unauthorized"}, status=HTTP_400_BAD_REQUEST)
        self.queryset = self.queryset.filter(room=room)
        return super().list(request, *args, **kwargs)

    def create_message(self, request, pk):
        room = Room.objects.filter(pk=pk).first()
        if not room:
            return Response({"error": "Topic not found"}, status=HTTP_400_BAD_REQUEST)
        if not room.members.filter(pk=request.user.pk).exists():
            return Response({"error": "Unauthorized"}, status=HTTP_400_BAD_REQUEST)
        self.queryset = self.queryset.filter(room=room)

        text = request.data.get("text")
        user = request.user
        serializer = self.serializer_class(data={"text": text, "room": room.pk, "created_by": user.pk})
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
