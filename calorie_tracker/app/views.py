from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Food
from django.db.models import Sum


def index(request):
    food = Food.objects.all()
    return render(request, "index.html", {"food": food, "kcal_sum": food.aggregate(Sum("kcal"))["kcal__sum"]})

def create(request):
    if request.method == "POST":
        food_item = Food()
        food_item.name = request.POST.get("name")
        food_item.kcal = request.POST.get("kcal")
        food_item.save()
    return HttpResponseRedirect("/")

def edit(request, id):
    try:
        food_item = Food.objects.get(id=id)

        if request.method == "POST":
            food_item.name = request.POST.get("name")
            food_item.kcal = request.POST.get("kcal")
            food_item.save()
            return HttpResponseRedirect("/")
        else:
            food = Food.objects.all()
            return render(request, "edit.html", {"food_item_to_edit": food_item, "food": food, "kcal_sum": food.aggregate(Sum("kcal"))["kcal__sum"]})
    except Food.DoesNotExist:
        return HttpResponseNotFound("<h2>Food not found</h2>")

def delete(request, id):
    try:
        food_item = Food.objects.get(id=id)
        food_item.delete()
        return HttpResponseRedirect("/")
    except Food.DoesNotExist:
        return HttpResponseNotFound("<h2>Food not found</h2>")
