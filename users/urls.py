# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from users import views as user_views

router = DefaultRouter()
router.register(r'usuarios', user_views.UserViewSet, basename='usuarios')

urlpatterns = [
    path('', include(router.urls))
]