from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
