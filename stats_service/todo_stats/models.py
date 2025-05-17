from django.db import models
from django.utils import timezone


class Stat(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    value = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'name'],
                name='unique_stat_name_per_user'
            )
        ]

    def __str__(self):
        return f"{self.name} (User: {self.user_id})"


class UserStat(models.Model):
    user_id = models.IntegerField()
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'stat'], name='unique_user_stat')
        ]

    def __str__(self):
        return f"{self.user_id} - {self.stat.name}: {self.value}"


class Item(models.Model):
    ITEM_TYPES = (
        ('AVATAR', 'Avatar'),
        ('BACKGROUND', 'Background'),
        ('FRAME', 'Frame'),
        ('BADGE', 'Badge'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=ITEM_TYPES)
    price = models.IntegerField()
    is_limited = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Shop(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def discounted_price(self):
        return self.price * (1 - self.discount / 100)

    def __str__(self):
        return f"{self.item.name} - {self.price} XP"


class UserInventory(models.Model):
    user_id = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_equipped = models.BooleanField(default=False)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'item')

    def __str__(self):
        return f"User {self.user_id} - {self.item.name}"


class UserAvatar(models.Model):
    user_id = models.IntegerField(unique=True)
    avatar = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='avatar_users')
    background = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='background_users')
    frame = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='frame_users')
    badges = models.ManyToManyField(Item, related_name='badge_users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User {self.user_id} Avatar" 