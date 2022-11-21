# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from . import views as product_views

router = DefaultRouter()
router.register(r'productos', product_views.ProductViewSet, basename='productos')

urlpatterns = [
    path('', include(router.urls))
]