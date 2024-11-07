from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StorageViewSet, OrganizationViewSet

router = DefaultRouter()
router.register(r'storages', StorageViewSet)
router.register(r'organizations', OrganizationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
