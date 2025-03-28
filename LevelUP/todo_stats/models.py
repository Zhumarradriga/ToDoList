from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


# Create your models here.
class Stat(models.Model):
    name = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey('todo_users.Users', on_delete=models.SET_NULL, null=True, blank=True)
    color = models.CharField(
        max_length=7,
        default='#000000',
        validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Цвет должен быть в формате HEX (#RRGGBB)')]
    )
    icon_id = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'Stats'
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by'], name='unique_stat_name_per_user')
        ]

    def __str__(self):
        return self.name
