from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users import views

app_name = 'users'

router_v1 = SimpleRouter()
router_v1.register('users', views.UserViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
]
