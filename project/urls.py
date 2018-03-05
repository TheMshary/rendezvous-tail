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

"""
Create event:				POST		/events
Retrieve list of events:	GET			/events
Retrieve specific event:	GET			/events/<id>
Update event:				PUT			/events/<id>
Delete event:				DELETE		/events/<id>

Invite to event:			POST		/events/<id>/invites
Uninvite:					DELETE  	/invites/<id>
Accept invite:				POST		/invites/<id>/accept
Decline invite:				POST		/invites/<id>/decline

Suggest in an event:		POST		/events/<id>/suggestions
Retrieve suggestions:		GET			/events/<id>/suggestions
Vote on suggestion:			POST		/suggestions/<id>/vote
Unvote on suggestion:		DELETE		/suggestions/<id>/vote
Delete suggestion:			DELETE		/suggestions/<id>

"""

urlpatterns = [
	url(r'^admin/', admin.site.urls),

	url(r'^events/$', views.EventView.as_view()),	# GET POST
	url(r'^events/(?P<event_id>\d+)/$', views.EventView.as_view()),	# GET PUT DELETE
	url(r'^events/(?P<event_id>\d+)/invites/$', views.InviteView.as_view()),	# POST

	url(r'^invites/(?P<invite_id>\d+)/$', views.InviteView.as_view()),	# DELETE
	url(r'^invites/(?P<invite_id>\d+)/accept/$', views.AcceptInviteView.as_view()),	# POST
	url(r'^invites/(?P<invite_id>\d+)/decline/$', views.DeclineInviteView.as_view()),	# POST

	url(r'^events/(?P<event_id>\d+)/suggestions/$', views.SuggestionView.as_view()),	# GET POST
	# url(r'^suggestions/(?P<suggestion_id>\d+)/$', views..as_view()),	# DELETE
	# url(r'^suggestions/(?P<suggestion_id>\d+)/vote/$', views..as_view()),	# POST DELETE


	# -------------------
	url(r'^register/', views.register),

	# Authenticating login (returns JsonResponse with token when username/password POST'd correctly)
	url(r'^login/alias/', views.AliasGetToken.as_view()),
	url(r'^login/', framework_views.obtain_auth_token),
]
