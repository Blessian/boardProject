from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import CursorPagination

from .models import Board, HashTag
from .serializers import \
    BoardCreateSerializer, BoardListSerializer, BoardRetrieveUpdateSerializer, BoardUpdateIsActiveSerializer
from common.permissions import IsOwner


class Pagination(CursorPagination):
    page_size = 10
    ordering = '-id'


# Create your views here.
class BoardViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ('writer', 'title')
    permission_classes = Pagination

    def get_serializer_class(self):
        if self.action == 'create':
            return BoardCreateSerializer
        if self.action == 'list':
            return BoardListSerializer
        if self.action in ['retrieve', 'update']:
            return BoardRetrieveUpdateSerializer
        if self.action == 'update_is_active':
            return BoardUpdateIsActiveSerializer

    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action in ['retrieve', 'update']:
            permission_classes = [IsOwner, IsAuthenticated]
        return [permission() for permission in permission_classes]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['writer'] = request.user.username
            serializer.validated_data['title'] = request.data['title']
            serializer.validated_data['content'] = request.data['content']
            board = Board()
            board.save(serializer)

            hash_tags = request.data['hash_tag']
            try:
                if hash_tags:
                    for hash_tag in hash_tags.split(','):
                        hash_tag_instance = HashTag()
                        hash_tag_instance.content = hash_tag

                        if HashTag.objects.get(content=hash_tag) > 0:
                            continue

                        hash_tag_instance.save()
                        board_db = Board.objects.get(id=board.id)
                        board_db.hash_tags.add(hash_tag)
            except TypeError:
                return Response(
                    serializer.data,
                    status.HTTP_400_BAD_REQUEST,
                    data={'error': '해시태그 작성 규칙을 확인해주세요'}
                )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=[], url_name='Update is_active')
    def update_is_active(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BoardUpdateIsActiveSerializer(
            data={'id': kwargs['id'], 'is_active': request.data['is_active']}
        )
        if serializer.is_valid(raise_exception=True):
            instance.is_active = serializer.validated_data['is_active']
            self.perform_update(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
