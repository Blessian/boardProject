from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

from common.models import User


# Create your models here.
class HashTag(models.Model):
    hash_tag_regex = RegexValidator(regex=r'^#[^\s]([,?\s?#0-9a-zA-Zㅏ-ㅣㄱ-ㅎ가-힣\s]*)[^\s]$')
    content = models.CharField(
        max_length=16,
        unique=True
    )


class Board(models.Model):
    writer = models.PositiveIntegerField()
    title = models.CharField(max_length=64)
    content = models.TextField()

    hash_tag = models.CharField(
        max_length=256,
        blank=True,
        help_text='해시태그는 #로 시작되고 , 로 구분됩니다. ex) #맛집,#서울,#브런치 카페,#주말, … '
    )
    hash_tags = models.ManyToManyField(HashTag, related_name='hash_tags', blank=True)

    create_date = models.DateTimeField(default=timezone.now())
    view_count = models.PositiveIntegerField(default=0)
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    like_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
