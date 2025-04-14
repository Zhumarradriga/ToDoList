from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StatViewSet, ItemViewSet, ShopViewSet,
    UserInventoryViewSet, UserAvatarViewSet
)

router = DefaultRouter()
router.register(r'stats', StatViewSet, basename='stat')
router.register(r'items', ItemViewSet, basename='item')
router.register(r'shop', ShopViewSet, basename='shop')
router.register(r'inventory', UserInventoryViewSet, basename='inventory')
router.register(r'avatar', UserAvatarViewSet, basename='avatar')

urlpatterns = [
    path('', include(router.urls)),
] 