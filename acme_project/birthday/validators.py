from django.core.exceptions import ValidationError

from datetime import date


def real_age(value: date) -> None:
    '''Проверка на реальный возраст (от 1 до 120 лет).'''
    age = (date.today() - value).days / 365
    if age < 1 or age > 120:
        raise ValidationError(
            'Ожидается возраст от 1 года до 120 лет'
        )
