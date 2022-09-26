from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='users')
urlpatterns = [
    path('', include((router.urls, 'common'))),
    # dj_rest_auth 로그인 url
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
]
