from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, Message
from accounts.serializers import UserSerializer


class ListRoomSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    topic = serializers.CharField(max_length=100)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    members = serializers.SerializerMethodField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["created_by"] = instance.created_by.username
        return data

    def get_members(self, instance):
        return instance.members.count()

class RoomSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    topic = serializers.CharField(max_length=100)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    members = serializers.SerializerMethodField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["created_by"] = instance.created_by.username
        return data

    def get_members(self, instance):
        users = instance.members.all()
        serializer = UserSerializer(users, many=True)
        return serializer.data

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

    def add_member(self, instance, user):
        instance.members.add(user)
        return instance

    def remove_member(self, instance, user):
        instance.members.remove(user)
        return instance


class MessageSerializer(serializers.Serializer):
    text = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["created_by"] = instance.created_by.username
        return data

    def create(self, validated_data):
        return Message.objects.create(**validated_data)
