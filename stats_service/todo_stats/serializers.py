from rest_framework import serializers
from .models import Stat, Item, Shop, UserInventory, UserAvatar


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['id', 'user_id', 'name', 'description', 'value', 'is_default', 'created_at', 'updated_at']
        read_only_fields = ('user_id', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.user_id != self.context['request'].user.id:
            raise serializers.PermissionDenied("You can only update your own stats")
        return super().update(instance, validated_data)


class ItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'type', 'price', 'is_limited', 'quantity', 'is_active', 'image', 'image_url', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at')

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None


class ShopSerializer(serializers.ModelSerializer):
    item_details = ItemSerializer(source='item', read_only=True)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'item', 'item_details', 'price', 'discount', 'discounted_price', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at')

    def get_discounted_price(self, obj):
        return obj.price * (1 - obj.discount / 100)


class UserInventorySerializer(serializers.ModelSerializer):
    item_details = ItemSerializer(source='item', read_only=True)

    class Meta:
        model = UserInventory
        fields = ['id', 'user_id', 'item', 'item_details', 'is_equipped', 'purchased_at']
        read_only_fields = ('user_id', 'purchased_at')

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)


class UserAvatarSerializer(serializers.ModelSerializer):
    avatar_details = ItemSerializer(source='avatar', read_only=True)
    background_details = ItemSerializer(source='background', read_only=True)
    frame_details = ItemSerializer(source='frame', read_only=True)
    badge_details = ItemSerializer(source='badges', many=True, read_only=True)

    class Meta:
        model = UserAvatar
        fields = ['id', 'user_id', 'avatar', 'avatar_details', 'background', 'background_details', 
                 'frame', 'frame_details', 'badges', 'badge_details', 'created_at', 'updated_at']
        read_only_fields = ('user_id', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data) 