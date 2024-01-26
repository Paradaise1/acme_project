from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from computed_property import ComputedTextField

from .utils import calculate_birthday_countdown
from .validators import real_age


User = get_user_model()


class Tag(models.Model):
    tag = models.CharField(max_length=20, verbose_name='Тег')

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.tag


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
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        blank=True,
        help_text='Удерживайте Ctrl для выбора нескольких вариантов',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint'
            ),
        )

        verbose_name = 'день рождения'
        verbose_name_plural = 'Дни рождения'

    @property
    def calculate(self):
        return str(calculate_birthday_countdown(self.birthday))

    def get_absolute_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    birthday = models.ForeignKey(
        Birthday, 
        on_delete=models.CASCADE,
        related_name='congratulations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
