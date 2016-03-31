from django.db import transaction
from django.db.models import Count

from django.shortcuts import render, redirect

# Create your views here.
import logging
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from donate.models import *


def signin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Username and password doesnt match")
    return redirect('login')


def register(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.POST['username'])
        if user:
            return HttpResponse("Username Already taken")

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    first_name=request.POST['name']
                )
                user.save()
        except:
            return HttpResponse("Error creating an account. Please register again")

        type = request.POST['type']
        context = {'user_name': request.POST['username']}
        context.update(csrf(request))
        if type == 'donor':
            donor = Donor(user=user)
            donor.save()
            return render(request, 'donor/contact.html', context)
        elif type == 'vol':
            volunteer = Volunteer(user=user)
            volunteer.save()
            return render(request, 'volunteer/contact.html', context)
        else:
            ngo = NGO(user=user)
            ngo.save()
            return render(request, 'ngo/contact.html', context)
    return redirect('signup')


def contact(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['user_name'])
        if hasattr(user, 'donor'):
            donor = user.donor
            donor.address = request.POST['address']
            donor.pincode = request.POST['pin']
            donor.phone = request.POST['phone']
            donor.save()
        elif hasattr(user, 'volunteer'):
            vol = user.volunteer
            vol.address = request.POST['address']
            vol.pincode = request.POST['pin']
            vol.phone = request.POST['phone']
            vol.save()
        elif hasattr(user, 'ngo'):
            ngo = user.ngo
            ngo.description = request.POST['description']
            ngo.phone = request.POST['phone']
            ngo.pincode = request.POST['pin']
            ngo.address = request.POST['address']
            # Image upload
            ngo.save()
        return redirect('login')
    return redirect('home')


def dashboard(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            return render(request, 'donor/donor.html')
        elif hasattr(user, 'volunteer'):
            # for deleting multiple elements, iterate through POST.keys(), and check if name attribute matches
            # Read Querydict docs
            pass
        elif hasattr(user, 'ngo'):
            context = {'ngo': user.ngo}
            return render(request, 'ngo/ngo.html', context)
    return redirect('login')


def create_ad(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'donor'):
                item = Item.objects.get(name=request.POST['itemname'])
                donation = Donation(
                    donor=user.donor,
                    item=item,
                    quantity=request.POST['quantity'],
                    description=request.POST['description'],
                    location=request.POST['address'],
                    contact=request.POST['phone'],
                )
                donation.save()
                return redirect('dashboard')
            return redirect('login')
    return redirect('home')


def create_event(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'ngo'):
                event = Event(
                    ngo=user.ngo,
                    type=request.POST['type'],
                    name=request.POST['name'],
                    location=request.POST['location'],
                    time=request.POST['time'],
                    description=request.POST['description']
                )
                event.save()
                return redirect('dashboard')
            return redirect('login')
    return redirect('home')


def settings(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'donor'):
                user.donor.pincode = request.POST['pincode']
                user.donor.phone = request.POST['phone']
                user.donor.address = request.POST['address']
                user.donor.save()
                if request.POST['new_password']:
                    user.set_password(request.POST['new_password'])
                    user.save()
            elif hasattr(user, 'volunteer'):
                user.volunteer.address = request.POST['address']
                user.volunteer.phone = request.POST['phone']
                user.volunteer.pincode = request.POST['pincode']
                user.volunteer.save()
                if request.POST['new_password']:
                    user.set_password(request.POST['new_password'])
                    user.save()
            elif hasattr(user, 'ngo'):
                user.first_name = request.POST['name']
                if request.POST['new_password']:
                    user.set_password(request.POST['new_password'])
                user.save()
                user.ngo.description = request.POST['description']
                user.ngo.phone = request.POST['phone']
                user.ngo.pincode = request.POST['pin']
                user.ngo.address = request.POST['address']
                # Image upload
                # Delete old image
                # Compare with contact.html and add/remove attributes
                user.ngo.save()
    return redirect('dashboard')


def view_events(request):
    user = request.user
    if user.is_authenticated():
        context = {'events': Event.objects.all()}
        if hasattr(user, 'donor'):
            return render(request, 'donor/viewEvents.html', context)
        elif hasattr(user, 'volunteer'):
            return render(request, 'ngo/viewEvents.html', context)
        elif hasattr(user, 'ngo'):
            return render(request, 'volunteer/viewEvents.html', context)
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('home')


def ngo_list(request):      # Donor
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'ngos': NGO.objects.all()}
            return render(request, 'donor/ngoList.html', context)
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('home')


def view_items(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'items': Item.objects.all()}
            return render(request, 'donor/items_required.html', context)
        elif hasattr(user, 'ngo'):
            context = {}
            return render(request, 'ngo/view-items.html', context)
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('home')


def edit_req(request):
    pass


def volunteer_event(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            if hasattr(user, 'volunteer'):
                # event =
                # user.volunteer.events_volunteered.add(event)
                # vol.save()
                pass
            return HttpResponse("User is not authorized to view the requested page")
    return redirect('home')


def log_out(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('home')


def about(request):
    if request.user.is_authenticated():
        context = {'logged_in': True}
    else:
        context = {'logged_in': False}
    return render(request, 'about.html', context)


def signup(request):
    context = {"error_message": ''}
    context.update(csrf(request))
    return render(request, 'register.html', context)


def home(request):
    print(request.user.username)
    if request.user.is_authenticated():
        return redirect('dashboard')
    else:
        return render(request, 'home.html')


def log_in(request):
    context = {"error_message": ''}
    context.update(csrf(request))
    return render(request, 'login.html', context)


def create_ad_view(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            items = Item.objects.all()
            context = {'donor': user.donor, 'items': items}
            context.update(csrf(request))
            return render(request, 'donor/create_ad.html', context)
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('login')


def create_event_view(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'ngo'):
            context = {}
            context.update(csrf(request))
            return render(request, 'ngo/create_event.html', context)
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('login')


def edit_req_view(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'ngo'):
            context = {}
            context.update(csrf(request))
            return render(request, 'ngo/editReq.html', context)
        return HttpResponse("User is not authorized to view the requested page")
    return redirect('login')


def settings_view(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            context = {'donor': user.donor}
            context.update(csrf(request))
            return render(request, 'donor/settings.html', context)
        elif hasattr(user, 'volunteer'):
            context = {'volunteer': user.volunteer}
            context.update(csrf(request))
            return render(request, 'volunteer/settings.html', context)
        elif hasattr(user, 'ngo'):
            context = {'ngo': user.ngo}
            context.update(csrf(request))
            return render(request, 'ngo/settings.html', context)
    return redirect('login')


def guidelines(request):
    user = request.user
    if user.is_authenticated():
        if hasattr(user, 'donor'):
            return render(request, 'donor/guidelines.html')
        elif hasattr(user, 'volunteer'):
            pass
        elif hasattr(user, 'ngo'):
            pass
    return redirect('login')


def join_as_vol(request):
    user = request.user
    if user.is_authenticated() and hasattr(user, 'donor'):
        logout(request)
        return redirect('signup')
    return redirect('login')


def faq(request):
    if request.user.is_authenticated():
        context = {'logged_in': True}
    else:
        context = {'logged_in': False}
    return render(request, 'faq.html', context)


def contact_us_view(request):
    if request.user.is_authenticated():
        context = {'logged_in': True}
    else:
        context = {'logged_in': False}
    context.update(csrf(request))
    return render(request, 'contact-form.html', context)


def contact_us(request):
    # send mail to ??
    pass
