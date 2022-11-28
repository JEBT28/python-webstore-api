# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from . import views as order_views

router = DefaultRouter()
router.register(r'orders', order_views.OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls))
]