from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users import views

app_name = 'users'

router_v1 = SimpleRouter()
router_v1.register('users', views.UserViewSet)


urlpatterns = [
    path('auth/token/login/', views.CustomTokenObtainPairView.as_view(),
         name='create_token'),
    path('auth/token/logout/', views.CustomTokenObtainPairView2.as_view(),
         name='delete_token'),
    path('', include(router_v1.urls)),
]
