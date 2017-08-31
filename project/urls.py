"""project URL Configuration

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

from rest_framework.authtoken import views as framework_views

from app import views 

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^event/', views.EventView.as_view()),
    url(r'^event/invite/', views.EventInviteView.as_view()),
    url(r'^event/suggest/', views.SuggestionView.as_view()),
    # url(r'^event/suggest/vote', views.VotingView.as_view()),

    url(r'^register/', views.register),

    # Authenticating login (returns JsonResponse with token when username/password POST'd correctly)
    url(r'^login/', framework_views.obtain_auth_token),
]
