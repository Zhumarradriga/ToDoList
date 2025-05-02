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
from logger import logger

class StatViewSet(viewsets.ModelViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.debug(f"Получение статистики для пользователя {self.request.user.id}")
        return Stat.objects.filter(user=self.request.user)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.debug("Получение списка предметов")
        return self.queryset

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.debug("Получение списка товаров в магазине")
        return self.queryset

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        shop_item = self.get_object()
        user = request.user
        logger.info(f"Попытка покупки предмета {shop_item.item.name} пользователем {user.id}")

        if user.points < shop_item.price:
            logger.warning(f"Недостаточно очков для покупки. У пользователя {user.id} {user.points} очков, требуется {shop_item.price}")
            return Response(
                {'error': 'Not enough points'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            UserInventory.objects.create(
                user=user,
                item=shop_item.item
            )
            user.points -= shop_item.price
            user.save()
            logger.info(f"Успешная покупка предмета {shop_item.item.name} пользователем {user.id}")
            return Response({'message': 'Purchase successful'})
        except Exception as e:
            logger.error(f"Ошибка при покупке предмета {shop_item.item.name} пользователем {user.id}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = UserInventorySerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.debug(f"Получение инвентаря пользователя {self.request.user.id}")
        return UserInventory.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def equip(self, request, pk=None):
        inventory_item = self.get_object()
        user = request.user
        logger.info(f"Попытка экипировки предмета {inventory_item.item.name} пользователем {user.id}")

        try:
            user_avatar, _ = UserAvatar.objects.get_or_create(user=user)

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
            logger.info(f"Предмет {inventory_item.item.name} успешно экипирован пользователем {user.id}")
            return Response({'message': 'Предмет успешно экипирован'})
        except Exception as e:
            logger.error(f"Ошибка при экипировке предмета {inventory_item.item.name} пользователем {user.id}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def unequip(self, request, pk=None):
        inventory_item = self.get_object()
        user = request.user
        logger.info(f"Попытка снятия предмета {inventory_item.item.name} пользователем {user.id}")

        try:
            user_avatar = UserAvatar.objects.get(user=user)
            
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
            logger.info(f"Предмет {inventory_item.item.name} успешно снят пользователем {user.id}")
            return Response({'message': 'Предмет успешно снят'})
        except UserAvatar.DoesNotExist:
            logger.error(f"Аватар пользователя {user.id} не найден")
            return Response(
                {'error': 'Аватар пользователя не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при снятии предмета {inventory_item.item.name} пользователем {user.id}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserAvatarViewSet(viewsets.ModelViewSet):
    serializer_class = UserAvatarSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.debug(f"Получение аватара пользователя {self.request.user.id}")
        return UserAvatar.objects.filter(user=self.request.user)

    def get_object(self):
        logger.debug(f"Получение объекта аватара пользователя {self.request.user.id}")
        return get_object_or_404(UserAvatar, user=self.request.user)

    @action(detail=False, methods=['post'])
    def update_avatar(self, request):
        avatar = self.get_object()
        item_id = request.data.get('item_id')
        logger.info(f"Попытка обновления аватара пользователя {request.user.id} на предмет {item_id}")
        
        try:
            item = Item.objects.get(id=item_id)
            if item.type != 'AVATAR':
                logger.warning(f"Неверный тип предмета {item_id} для аватара")
                return Response(
                    {'error': 'Invalid item type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not UserInventory.objects.filter(user=request.user, item=item).exists():
                logger.warning(f"Предмет {item_id} отсутствует в инвентаре пользователя {request.user.id}")
                return Response(
                    {'error': 'Item not in inventory'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            avatar.avatar = item
            avatar.save()
            logger.info(f"Аватар пользователя {request.user.id} успешно обновлен на предмет {item_id}")
            return Response(self.get_serializer(avatar).data)
            
        except Item.DoesNotExist:
            logger.error(f"Предмет {item_id} не найден")
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при обновлении аватара пользователя {request.user.id}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def update_background(self, request):
        avatar = self.get_object()
        item_id = request.data.get('item_id')
        logger.info(f"Попытка обновления фона пользователя {request.user.id} на предмет {item_id}")
        
        try:
            item = Item.objects.get(id=item_id)
            if item.type != 'BACKGROUND':
                logger.warning(f"Неверный тип предмета {item_id} для фона")
                return Response(
                    {'error': 'Invalid item type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not UserInventory.objects.filter(user=request.user, item=item).exists():
                logger.warning(f"Предмет {item_id} отсутствует в инвентаре пользователя {request.user.id}")
                return Response(
                    {'error': 'Item not in inventory'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            avatar.background = item
            avatar.save()
            logger.info(f"Фон пользователя {request.user.id} успешно обновлен на предмет {item_id}")
            return Response(self.get_serializer(avatar).data)
            
        except Item.DoesNotExist:
            logger.error(f"Предмет {item_id} не найден")
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при обновлении фона пользователя {request.user.id}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def update_frame(self, request):
        avatar = self.get_object()
        item_id = request.data.get('item_id')
        logger.info(f"Попытка обновления рамки пользователя {request.user.id} на предмет {item_id}")
        
        try:
            item = Item.objects.get(id=item_id)
            if item.type != 'FRAME':
                logger.warning(f"Неверный тип предмета {item_id} для рамки")
                return Response(
                    {'error': 'Invalid item type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not UserInventory.objects.filter(user=request.user, item=item).exists():
                logger.warning(f"Предмет {item_id} отсутствует в инвентаре пользователя {request.user.id}")
                return Response(
                    {'error': 'Item not in inventory'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            avatar.frame = item
            avatar.save()
            logger.info(f"Рамка пользователя {request.user.id} успешно обновлена на предмет {item_id}")
            return Response(self.get_serializer(avatar).data)
            
        except Item.DoesNotExist:
            logger.error(f"Предмет {item_id} не найден")
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при обновлении рамки пользователя {request.user.id}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def toggle_badge(self, request):
        avatar = self.get_object()
        item_id = request.data.get('item_id')
        logger.info(f"Попытка переключения значка пользователя {request.user.id} на предмет {item_id}")
        
        try:
            item = Item.objects.get(id=item_id)
            if item.type != 'BADGE':
                logger.warning(f"Неверный тип предмета {item_id} для значка")
                return Response(
                    {'error': 'Invalid item type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not UserInventory.objects.filter(user=request.user, item=item).exists():
                logger.warning(f"Предмет {item_id} отсутствует в инвентаре пользователя {request.user.id}")
                return Response(
                    {'error': 'Item not in inventory'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if item in avatar.badges.all():
                avatar.badges.remove(item)
                logger.info(f"Значок {item_id} снят с пользователя {request.user.id}")
            else:
                avatar.badges.add(item)
                logger.info(f"Значок {item_id} добавлен пользователю {request.user.id}")
            
            return Response(self.get_serializer(avatar).data)
            
        except Item.DoesNotExist:
            logger.error(f"Предмет {item_id} не найден")
            return Response(
                {'error': 'Item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Ошибка при переключении значка пользователя {request.user.id}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 