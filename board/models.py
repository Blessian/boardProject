from django.db import models
from django.core.validators import RegexValidator

from common.models import User
from datetime import datetime


# Create your models here.
class Board(models.Model):
    writer = models.PositiveIntegerField()
    title = models.CharField(max_length=64)
    content = models.TextField()

    hash_tag_regex = RegexValidator(regex=r'#([0-9a-zA-Zㅏ-ㅣㄱ-ㅎ가-힣\s]*),')
    hash_tag = models.CharField(
        max_length=256,
        help_text='해시태그는 #로 시작되고 , 로 구분됩니다. ex) #맛집,#서울,#브런치 카페,#주말, … '
    )

    create_datetime = models.DateTimeField(default=datetime.now())
    view_count = models.PositiveIntegerField(default=0)
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    like_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
