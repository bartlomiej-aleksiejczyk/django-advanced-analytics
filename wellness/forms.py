from django import forms
from .models import Meal, CalorieLimit


class DateInput(forms.DateInput):
    input_type = "date"


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["eaten_on", "name", "calories"]
        widgets = {
            "eaten_on": DateInput(),
        }


class CalorieLimitForm(forms.ModelForm):
    class Meta:
        model = CalorieLimit
        fields = ["start_date", "end_date", "calories_per_day"]
        widgets = {
            "start_date": DateInput(),
            "end_date": DateInput(),
        }
