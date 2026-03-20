from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Meal(models.Model):
    eaten_on = models.DateField(default=timezone.localdate)
    name = models.CharField(max_length=120)
    calories = models.PositiveIntegerField()

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.name} ({self.calories} kcal)"


class CalorieLimit(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    calories_per_day = models.PositiveIntegerField()

    class Meta:
        ordering = ["-start_date"]

    def __str__(self) -> str:
        return f"{self.calories_per_day} kcal: {self.start_date} - {self.end_date}"

    def clean(self) -> None:
        super().clean()

        if self.end_date < self.start_date:
            raise ValidationError(
                {"end_date": "End date must be greater than or equal to start date."}
            )

        overlapping_limits = CalorieLimit.objects.filter(
            Q(start_date__lte=self.end_date) & Q(end_date__gte=self.start_date)
        )

        if self.pk:
            overlapping_limits = overlapping_limits.exclude(pk=self.pk)

        if overlapping_limits.exists():
            raise ValidationError(
                "This calorie limit overlaps with another existing calorie limit."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
