from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm

from snowplow_tracker import Tracker, Emitter, Subject

def init_tracker(request):
    emitter = Emitter("micro", port=9090)
    subject = Subject().set_platform("web").set_user_id(request.user.username)

    tracker = Tracker(emitter,
                    subject=subject,
                    app_id="fridge",
                    encode_base64=False)
    return tracker

def logout_view(request):
    """Log the user out.
    """
    tracker = init_tracker(request)
    tracker.track_link_click("http://0.0.0.0:8000/log_out", "log_out_click")
    logout(request)
    return HttpResponseRedirect(reverse('my_fridge:home'))


def register(request):
    """Register a new user.
    """
    tracker = init_tracker(request)
    tracker.track_page_view("http://0.0.0.0:8000/register", "register_user")
    if request.method != 'POST':
        # Display blank registration form.
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Log the user in and then redirect to home page.
            authenticate_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse('my_fridge:home'))

    context = {'form': form}
    return render(request, 'users/register.html', context)
