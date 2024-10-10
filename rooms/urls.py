from django.urls import path

from .viewsets import AdminRoomViewSet, UserRoomViewSet, MessageViewSet

urlpatterns = [
    path("admin/", AdminRoomViewSet.as_view({"post": "create_room"})),
    path("admin/<int:pk>/member/", AdminRoomViewSet.as_view({"post": "add_member", "delete": "remove_member"})),
    path("admin/<int:pk>/", AdminRoomViewSet.as_view({"delete": "delete_room"})),
    path("", UserRoomViewSet.as_view({"get": "list"})),
    path("<int:pk>/", UserRoomViewSet.as_view({"get": "retrieve_room"})),
    path("<int:pk>/subscribe/", UserRoomViewSet.as_view({"post": "subscribe_topic"})),
    path("<int:pk>/unsubscribe/", UserRoomViewSet.as_view({"post": "unsubscribe_topic"})),
    path("<int:pk>/message/", MessageViewSet.as_view({"get": "list", "post": "create_message"})),
]
