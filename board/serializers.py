from rest_framework import serializers

from .models import Board


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['writer', 'title', 'content', 'hash_tag']


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'writer', 'title', 'hash_tag', 'create_date', 'like_count', 'view_count']


class BoardRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ['id', 'writer', 'create_date', 'like', 'like_count', 'view_count', 'is_active']


class BoardUpdateIsActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'is_active']
