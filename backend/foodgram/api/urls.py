from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api import views

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register('recipes', views.RecipeViewSet, basename='recipes')
router_v1.register('tags', views.TagViewSet, basename='tags')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('users.urls')),
]
