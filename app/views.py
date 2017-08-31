#============================= CORE IMPORTS =============================#
import json
from itertools import chain

#============================ Django IMPORTS ==============================#
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

#======================== REST FRAMEWORK IMPORTS ========================#
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView


#============================= APP IMPORTS ==============================#
from app.serializers import *

# Create your views here.

class EventView(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	# Return single event if 'pk' parameter specified
	# Return all events if no 'pk' specified
	def get(self, request):
		# request.user is the loggedin user
		# request.auth is the auth token of that user

		eventpk = request.GET.get('pk')
		user = request.user
		if eventpk is None:
			events_created = user.events_created
			events_attending = user.events_attending
			
			events = Event.objects.filter(Q(creator=user) | Q(attendees=user))
			serializer = EventSerializer(events, many=True)

		else:
			event = get_object_or_404(Event, pk=eventpk)
			serializer = EventSerializer(event)

		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = EventSerializer(data=request.data)
		if serializer.is_valid():
			event = serializer.save()
			event.creator = request.user
			event.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventInviteView(APIView):

	def post(self, request):
		pk = request.data.get('pk')
		usernames = request.data.get('invitees')
		event = Event.objects.get(pk=pk)
		for username in usernames:
			invitee = User.objects.get(username=username)
			event.attendees.add(invitee)

		return Response(status=status.HTTP_201_CREATED)


class SuggestionView(APIView):

	# you get suggestions when GET-ing the Event, so this get function might not be needed
	def get(self, request):
		eventpk = request.data.get('pk')
		suggestions = Suggestion.objects.filter(event__pk=eventpk)
		serializer = SuggestionSerializer(suggestions, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = SuggestionSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class VotingView(APIView):

# 	def post(self, request):
# 		pk = request.data.get('pk')
# 		usernames = request.data.get('invitees')
# 		event = Event.objects.get(pk=pk)
# 		for username in usernames:
# 			invitee = User.objects.get(username=username)
# 			event.attendees.add(invitee)

# 		return Response(status=status.HTTP_201_CREATED)

@api_view(["POST"])
@csrf_exempt
@permission_classes((AllowAny,))
def register(request):
	try:
		User.objects.get(username=request.data.get("username"))
		return Response({'msg':"Username taken."}, status=status.HTTP_400_BAD_REQUEST)
	except User.DoesNotExist:
		pass

	serializer = UserSerializer(data=request.data)
	if serializer.is_valid():
		user_instance = serializer.save()
		user_instance.set_password(request.POST.get("password"))
		user_instance.save()
		# user_instance.profile.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


