from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Stat, Item, Shop, UserInventory, UserAvatar
from .serializers import (
    StatSerializer, ItemSerializer, ShopSerializer,
    UserInventorySerializer, UserAvatarSerializer
)
from .authentication import CustomJWTAuthentication

class StatViewSet(viewsets.ModelViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Stat.objects.filter(user=self.request.user)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        shop_item = self.get_object()
        user = request.user

        if user.points < shop_item.price:
            return Response(
                {'error': 'Not enough points'},
                status=status.HTTP_400_BAD_REQUEST
            )

        UserInventory.objects.create(
            user=user,
            item=shop_item.item
        )

        user.points -= shop_item.price
        user.save()

        return Response({'message': 'Purchase successful'})

class UserInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = UserInventorySerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInventory.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def equip(self, request, pk=None):
        inventory_item = self.get_object()
        user = request.user

        # Получаем или создаем аватар пользователя
        user_avatar, _ = UserAvatar.objects.get_or_create(user=user)

        # Экипируем предмет в зависимости от его типа
        if inventory_item.item.type == 'AVATAR':
            user_avatar.avatar = inventory_item.item
        elif inventory_item.item.type == 'BACKGROUND':
            user_avatar.background = inventory_item.item
        elif inventory_item.item.type == 'FRAME':
            user_avatar.frame = inventory_item.item
        elif inventory_item.item.type == 'BADGE':
            user_avatar.badges.add(inventory_item.item)

        user_avatar.save()
        inventory_item.is_equipped = True
        inventory_item.save()

        return Response({'message': 'Предмет успешно экипирован'})

    @action(detail=True, methods=['post'])
    def unequip(self, request, pk=None):
        inventory_item = self.get_object()
        user = request.user

        try:
            user_avatar = UserAvatar.objects.get(user=user)
            
            # Снимаем предмет в зависимости от его типа
            if inventory_item.item.type == 'AVATAR':
                user_avatar.avatar = None
            elif inventory_item.item.type == 'BACKGROUND':
                user_avatar.background = None
            elif inventory_item.item.type == 'FRAME':
                user_avatar.frame = None
            elif inventory_item.item.type == 'BADGE':
                user_avatar.badges.remove(inventory_item.item)

            user_avatar.save()
            inventory_item.is_equipped = False
            inventory_item.save()

            return Response({'message': 'Предмет успешно снят'})
        except UserAvatar.DoesNotExist:
            return Response(
                {'error': 'Аватар пользователя не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

class UserAvatarViewSet(viewsets.ModelViewSet):
    serializer_class = UserAvatarSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAvatar.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(UserAvatar, user=self.request.user)

    @action(detail=False, methods=['post'])
    def update_avatar(self, request):
        avatar = self.get_object()
        item_id = request.data.get('item_id')
        
        try:
            item = Item.objects.get(id=item_id)
            if item.type != 'AVATAR':
                return Response(
                    {'error': 'Invalid item type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not UserInventory.objects.filter(user=request.user, item=item).exists():
                return Response(
                    {'error': 'Item not in inventory'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            avatar.avatar = item
            avatar.save()
            return Response(self.get_serializer(avatar).data)
            
        except Item.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def update_background(self, request):
        avatar = self.get_object()
        item_id = request.data.get('item_id')
        
        try:
            item = Item.objects.get(id=item_id)
            if item.type != 'BACKGROUND':
                return Response(
                    {'error': 'Invalid item type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not UserInventory.objects.filter(user=request.user, item=item).exists():
                return Response(
                    {'error': 'Item not in inventory'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            avatar.background = item
            avatar.save()
            return Response(self.get_serializer(avatar).data)
            
        except Item.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def update_frame(self, request):
        avatar = self.get_object()
        item_id = request.data.get('item_id')
        
        try:
            item = Item.objects.get(id=item_id)
            if item.type != 'FRAME':
                return Response(
                    {'error': 'Invalid item type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not UserInventory.objects.filter(user=request.user, item=item).exists():
                return Response(
                    {'error': 'Item not in inventory'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            avatar.frame = item
            avatar.save()
            return Response(self.get_serializer(avatar).data)
            
        except Item.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def toggle_badge(self, request):
        avatar = self.get_object()
        item_id = request.data.get('item_id')
        
        try:
            item = Item.objects.get(id=item_id)
            if item.type != 'BADGE':
                return Response(
                    {'error': 'Invalid item type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not UserInventory.objects.filter(user=request.user, item=item).exists():
                return Response(
                    {'error': 'Item not in inventory'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if item in avatar.badges.all():
                avatar.badges.remove(item)
            else:
                avatar.badges.add(item)
            
            return Response(self.get_serializer(avatar).data)
            
        except Item.DoesNotExist:
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            ) 