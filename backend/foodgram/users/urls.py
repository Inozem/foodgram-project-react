from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users import views

app_name = 'users'

router_v1 = SimpleRouter()
router_v1.register('users', views.CustomUserViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
