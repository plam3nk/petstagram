from enum import Enum

from django.core import validators
from django.db import models
from django.contrib.auth import models as auth_models


def validate_only_alphabetical(value):
    pass


class ChoicesMixin:
    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]


class ChoicesStringsMixin(ChoicesMixin):
    @classmethod
    def max_length(cls):
        return max(len(choice.value) for choice in cls)


class Gender(ChoicesStringsMixin, Enum):
    MALE = 'male'
    FEMALE = 'female'
    DO_NOT_SHOW = 'do not show'


# class Another(Enum, ChoicesMixin):
#     Choice1 = 1
#     Choice2 = 2


# Create your models here.

class PetstagramUser(auth_models.AbstractUser):
    FIRST_NAME_MIN_LEN = 2
    FIRST_NAME_MAX_LEN = 30
    LAST_NAME_MIN_LEN = 2
    LAST_NAME_MAX_LEN = 30
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=(
            validators.MinLengthValidator(FIRST_NAME_MIN_LEN),
            validate_only_alphabetical,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=(
            validators.MinLengthValidator(LAST_NAME_MIN_LEN),
            validate_only_alphabetical,
        )
    )

    email = models.EmailField(
        unique=True
    )

    gender = models.CharField(
        choices=Gender.choices(),
        max_length=Gender.max_length(),
    )

    profile_picture = models.URLField(
        null=True,
        blank=True,
    )

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        return None

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)

        # Variant 2
        # Send email on successful register
        # Good enough, but there is a better option (signals)
        # send_mail...

        return result

