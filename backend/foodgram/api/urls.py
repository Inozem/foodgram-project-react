from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api import views

app_name = 'api'

# router_v1 = SimpleRouter()
# router_v1.register('auth/signup', views.UserViewSet, basename='signup')


urlpatterns = [
    path('', include('users.urls')),
    # path('', include('djoser.urls')),
]
