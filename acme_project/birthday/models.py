from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from computed_property import ComputedTextField

from .utils import calculate_birthday_countdown
from .validators import real_age


User = get_user_model()


class Birthday(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(
        blank=True,
        help_text='Необязательное поле',
        max_length=20,
        verbose_name='Фамилия'
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
        validators=(real_age,)
    )
    days_left_for_birthday = ComputedTextField(compute_from='calculate')
    image = models.ImageField(
        blank=True,
        upload_to='birthdays_images',
        verbose_name='Фото'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор записи',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint'
            ),
        )

    @property
    def calculate(self):
        return str(calculate_birthday_countdown(self.birthday))

    def get_absolute_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.pk})
    
