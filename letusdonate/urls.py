"""letusdonate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from donate.views import *

urlpatterns = [
    #Same for all
    url(r'^admin/', admin.site.urls),
    url(r'^signin$', signin, name="signin"),
    url(r'^register', register, name="register"),
    url(r'^logout$', log_out, name="logout"),
    url(r'^$', home, name="home"),  # Before logging in
    url(r'^signup$', signup, name="signup"),
    url(r'^about$', about, name="about"),
    url(r'^faq$', faq, name="faq"),
    url(r'^contact_us_response$', contact_us, name="contact_us"),

    #Dummy views
    url(r'^login$', log_in, name="login"),
    url(r'^create_ads', create_ad_view, name="create_ad_view"),     # Donor
    url(r'^create_events$', create_event_view, name="create_event_view"),  # NGO
    url(r'^requirements$', edit_req_view, name="edit_req_view"),    # NGO
    url(r'^contact_us$', contact_us_view, name="contact_us_view"),

    #user specific
    url(r'^create_event$', create_event, name="create_event"),  # NGO
    url(r'^create_ad$', create_ad, name="create_ad"),   # Donor
    url(r'^join_as_vol$', join_as_vol, name="join_as_vol"),     # Donor
    url(r'^events$', view_events, name="view_events"),    # Donor
    url(r'^ngos$', ngo_list, name="ngo_list"),   # Donor
    url(r'^edit_requirements$', edit_req, name="edit_req"),    # NGO
    url(r'^volunteer_event$', volunteer_event, name="volunteer_event"),     # Volunteer

    #different view for each user
    url(r'^contact$', contact, name="contact"),  # Donor,volunteer contact: To be shown after signup
    url(r'^dashboard/?$', dashboard, name="dashboard"),
    url(r'^change_settings$', settings, name="settings"),
    url(r'^guidelines$', guidelines, name="guidelines"),
    url(r'^settings$', settings_view, name="settings_view"),
    url(r'^items$', view_items, name="view_items"),     # List of items available for donation
]

