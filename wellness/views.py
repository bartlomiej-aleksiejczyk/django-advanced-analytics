from django.http import HttpResponse
from django.shortcuts import render

from datetime import date, timedelta

from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import MealForm, CalorieLimitForm
from .models import Meal, CalorieLimit


# Create your views here.
def wellness_index(request) -> HttpResponse:
    return render(request, "wellness/wellness_index.html")


def calorie_tracker(request):
    day_str = request.GET.get("day")
    try:
        selected_day = date.fromisoformat(day_str) if day_str else timezone.localdate()
    except ValueError:
        selected_day = timezone.localdate()

    edit_meal_id = request.GET.get("edit")
    edit_meal = None

    if edit_meal_id:
        edit_meal = get_object_or_404(Meal, pk=edit_meal_id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_meal":
            form = MealForm(request.POST)
            if form.is_valid():
                meal = form.save()
                return redirect(
                    f"{reverse('wellness:calorie_tracker')}?day={meal.eaten_on.isoformat()}"
                )

        elif action == "edit_meal":
            meal_id = request.POST.get("meal_id")
            meal = get_object_or_404(Meal, pk=meal_id)
            form = MealForm(request.POST, instance=meal)
            if form.is_valid():
                meal = form.save()
                return redirect(
                    f"{reverse('wellness:calorie_tracker')}?day={meal.eaten_on.isoformat()}"
                )

        elif action == "delete_meal":
            meal_id = request.POST.get("meal_id")
            meal = get_object_or_404(Meal, pk=meal_id)
            redirect_day = meal.eaten_on
            meal.delete()
            return redirect(
                f"{reverse('wellness:calorie_tracker')}?day={redirect_day.isoformat()}"
            )

    add_form = MealForm(initial={"eaten_on": selected_day})
    edit_form = MealForm(instance=edit_meal) if edit_meal else None

    meals = Meal.objects.filter(eaten_on=selected_day).order_by("id")
    total_calories = meals.aggregate(total=Sum("calories"))["total"] or 0

    active_limit = CalorieLimit.objects.filter(
        start_date__lte=selected_day,
        end_date__gte=selected_day,
    ).first()

    previous_day = selected_day - timedelta(days=1)
    next_day = selected_day + timedelta(days=1)

    context = {
        "selected_day": selected_day,
        "previous_day": previous_day,
        "next_day": next_day,
        "meals": meals,
        "total_calories": total_calories,
        "active_limit": active_limit,
        "remaining_calories": (
            active_limit.calories_per_day - total_calories if active_limit else None
        ),
        "add_form": add_form,
        "edit_form": edit_form,
        "edit_meal": edit_meal,
    }
    return render(request, "wellness/calorie_tracker.html", context)


def calorie_limits(request):
    edit_limit_id = request.GET.get("edit")
    edit_limit = None

    if edit_limit_id:
        edit_limit = get_object_or_404(CalorieLimit, pk=edit_limit_id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_limit":
            form = CalorieLimitForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("wellness:calorie_limits")

        elif action == "edit_limit":
            limit_id = request.POST.get("limit_id")
            limit_instance = get_object_or_404(CalorieLimit, pk=limit_id)
            form = CalorieLimitForm(request.POST, instance=limit_instance)
            if form.is_valid():
                form.save()
                return redirect("wellness:calorie_limits")

        elif action == "delete_limit":
            limit_id = request.POST.get("limit_id")
            limit_instance = get_object_or_404(CalorieLimit, pk=limit_id)
            limit_instance.delete()
            return redirect("wellness:calorie_limits")

    add_form = CalorieLimitForm()
    edit_form = CalorieLimitForm(instance=edit_limit) if edit_limit else None

    limits = CalorieLimit.objects.all()

    context = {
        "limits": limits,
        "add_form": add_form,
        "edit_form": edit_form,
        "edit_limit": edit_limit,
    }
    return render(request, "wellness/calorie_limits.html", context)
