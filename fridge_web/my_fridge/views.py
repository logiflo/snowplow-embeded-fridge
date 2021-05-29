from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import Food, Essencial
from .forms import FoodForm, QuantityForm, EssencialForm, QuantityEssencialForm

from snowplow_tracker import Tracker, Emitter, Subject


def init_tracker(request):
    emitter = Emitter("micro", port=9090)
    subject = Subject().set_platform("web").set_user_id(request.user.username)

    tracker = Tracker(emitter,
                    subject=subject,
                    app_id="fridge",
                    encode_base64=False)
    return tracker
    #    namespace="cf",
    #    app_id="frigde",)


def home(request):
    """The home page for My Fridge
    """
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/home", "home_page")
    return render(request, 'my_fridge/home.html')


@login_required
def food(request):
    """Show food.
    """
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/food", "food_page")
    food = Food.objects.filter(owner=request.user).order_by('date_added')
    is_empty = True
    for f in food:
        if f.quantity > 0:
            is_empty = False
            break
    context = {'food': food, 'is_empty': is_empty}
    return render(request, 'my_fridge/food.html', context)


@login_required
def essencials(request):
    """Show essencials.
    """
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/essencials", "essencials_page")
    essencial = Essencial.objects.filter(
        owner=request.user).order_by('date_added')
    is_empty = True
    for e in essencial:
        is_empty = False
        break
    context = {'essencial': essencial, 'is_empty': is_empty}
    return render(request, 'my_fridge/essencials.html', context)


@login_required
def food_out(request):
    """Show food run out.
    """
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/food_out", "food_out_page")
    food = Food.objects.filter(owner=request.user).order_by('date_added')
    context = {'food': food}
    return render(request, 'my_fridge/food_out.html', context)


@login_required
def add_food(request):
    """Add food
    """
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/add_food", "add_food_page")
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = FoodForm()
    else:
        # POST data submitted; process data.
        form = FoodForm(request.POST)
        if form.is_valid():
            new_food = form.save(commit=False)
            new_food.owner = request.user
            new_food.save()

            return HttpResponseRedirect(reverse('my_fridge:food'))

    context = {'form': form}
    return render(request, 'my_fridge/add_food.html', context)


@login_required
def add_essencials(request):
    """Add essencials
    """
    tracker = init_tracker(request)
    # tracker.track_link_click("my_fridge/add_essencials.html")
    tracker.track_page_view("http://0.0.0.0:8000/add_essencials", "add_essencials_page")

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EssencialForm()
    else:
        # POST data submitted; process data.
        form = EssencialForm(request.POST)
        if form.is_valid():
            new_essencial = form.save(commit=False)
            new_essencial.owner = request.user
            new_essencial.save()

            return HttpResponseRedirect(reverse('my_fridge:essencials'))

    context = {'form': form}
    return render(request, 'my_fridge/add_essencials.html', context)


@login_required
def each_food(request, food_id):
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/each_food/<food_id>", "each_food_page")
    """Show food and its current quantity.
    """
    food = Food.objects.get(id=food_id)

    context = {'food': food}
    return render(request, 'my_fridge/each_food.html', context)


@login_required
def add_quantity(request, food_id):
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/add_quantity/<food_id>", "add_quantity_page")
    food = Food.objects.get(id=food_id)
    if food.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = FoodForm(instance=food)
        form.fields['text'].widget.attrs['readonly'] = True
    else:
        # POST data submitted; process data.
        form = FoodForm(request.POST, instance=food)
        form.fields['text'].widget.attrs['readonly'] = True
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('my_fridge:food'))

    context = {'food': food, 'form': form}
    return render(request, 'my_fridge/add_quantity.html', context)


@login_required
def add_quantity_essencials(request, essencials_id):
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/add_quantity_essencials/<essencials_id>", "add_quantity_essencials_page")
    essencials = Essencial.objects.get(id=essencials_id)
    if essencials.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EssencialForm(instance=essencials)
        form.fields['text'].widget.attrs['readonly'] = True
    else:
        # POST data submitted; process data.
        form = EssencialForm(request.POST, instance=essencials)
        form.fields['text'].widget.attrs['readonly'] = True
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('my_fridge:essencials'))

    context = {'form': form, 'essencials': essencials}
    return render(request, 'my_fridge/add_quantity_essencials.html', context)


@login_required
def add_essencials_to_fridge(request):
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/add_essencials_to_fridge", "add_essencials_to_fridge_page")
    essencials = Essencial.objects.all()
    food = Food.objects.all()

    id_obj_error = list()
    id_essencial_error = list()
    is_error = 0

    for essencial in essencials:
        if essencial.owner != request.user:
            raise Http404

        obj, created = Food.objects.get_or_create(text__exact=essencial.text, defaults={
                                                  'text': essencial.text, 'units': essencial.units, 'quantity': essencial.quantity, 'owner': essencial.owner})
        if not created:
            if obj.owner != request.user:
                raise Http404
            if obj.units == essencial.units:
                if obj.quantity < essencial.quantity:
                    obj.quantity = essencial.quantity
                    obj.save(update_fields=['quantity'])
            else:
                is_error += 1
                id_obj_error.append(obj.id)
                id_essencial_error.append(essencial.id)
    obj_error = Food.objects.filter(pk__in=id_obj_error)
    essencial_error = Essencial.objects.filter(pk__in=id_essencial_error)
    list_error = zip(obj_error, essencial_error)
    context = {'is_error': is_error, 'list_error': list_error}
    return render(request, 'my_fridge/add_essentials_to_fridge.html', context)


@login_required
def change_units(request, food_id):
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/change_unit/<food_id>", "change_unit_page")
    food = Food.objects.get(id=food_id)
    if food.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = FoodForm(instance=food)
        form.fields['text'].widget.attrs['readonly'] = True
    else:
        # POST data submitted; process data.
        form = EssencialForm(request.POST, instance=food)
        form.fields['text'].widget.attrs['readonly'] = True

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('my_fridge:essencials'))

    context = {'form': form, 'food': food}
    return render(request, 'my_fridge/change_units.html', context)


@login_required
def remove_food(request, food_id):
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/remove_food/<food_id>", "remove_food_page")
    food = Food.objects.get(id=food_id)
    if food.owner != request.user:
        raise Http404

    food.delete()

    context = {'food': food}
    return render(request, 'my_fridge/remove_food.html', context)


@login_required
def remove_essencial(request, essencials_id):
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/remove_essencial/<essencials_id>", "remove_essencial_page")
    essencial = Essencial.objects.get(id=essencials_id)
    if essencial.owner != request.user:
        raise Http404

    essencial.delete()

    context = {'essencial': essencial}
    return render(request, 'my_fridge/remove_essencial.html', context)
