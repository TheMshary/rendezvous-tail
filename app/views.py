#============================= CORE IMPORTS =============================#
import json
import requests
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
from app.models import *

# Create your views here.

class EventView(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	# Return single event if 'pk' parameter specified
	# Return all events if no 'pk' specified
	def get(self, request, event_id=None):
		# request.user is the loggedin user
		# request.auth is the auth token of that user

		user = request.user
		if event_id is None:
			events_created = user.events_created.order_by("time")
			events_attending = user.invite_set.filter(status="accepted").order_by("event__time")

			# events = Event.objects.filter(Q(creator=user) | Q(attendees=user)).distinct()
			# serializer = EventSerializer(events, many=True)
			serializer_created = EventSerializer(events_created, many=True)
			serializer_attending = EventSerializer(events_attending, many=True)
			invites = Invite.objects.filter(status="pending", user=user)
			serializer_invites = InviteSerializer(invites, many=True)
			data = {
				"created": serializer_created.data,
				"attending": serializer_attending.data,
				"invites": serializer_invites.data
			}
		else:
			event = get_object_or_404(Event, pk=event_id)
			serializer = EventSerializer(event)
			data = serializer.data
			event_invitees = event.get_invitees()
			event_attendees = event.get_attendees()
			event_invitees_serializer = InviteSerializer(event_invitees, many=True)
			event_attendees_serializer = InviteSerializer(event_attendees, many=True)
			data.update({
				"invitees": event_invitees_serializer.data,
				"attendees": event_attendees_serializer.data
			})

		return Response(data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = EventSerializer(data=request.data)
		if serializer.is_valid():
			event = serializer.save()
			event.creator = request.user
			event.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, event_id):
		event = get_object_or_404(Event, id=event_id)
		serializer = EventSerializer(event, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, event_id):
		event = get_object_or_404(Event, id=event_id)
		event.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)

class InviteView(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	# this post() doesn't do bulk invites
	# def post(self, request, event_id):
	# 	username = request.data.get('invitee')
	# 	event = get_object_or_404(Event, pk=event_id)
	# 	user = get_object_or_404(User, username=username)
	# 	invite = Invite.objects.create(event=event, user=user)
	# 	invite.save()

	# 	serializer = InviteSerializer(invite)
	# 	return Response(serializer.data, status=status.HTTP_201_CREATED)


	# this post() does bulk invites
	def post(self, request, event_id):
		usernames = request.data.get('invitees')
		event = Event.objects.get(pk=event_id)
		already_invited = []

		if "invitees" in request.data and len(usernames) > 0:	# Checks if there are invitees specified
			for username in usernames:
				user = User.objects.get(username=username)
				if not Invite.objects.filter(event=event, user=user).exists():
					invite = Invite.objects.create(event=event, user=user)
					invite.save()
				else:
					already_invited.append(username)
		else:
			error = {
				"msg": "Must enter at least one username to invite."
			}
			return Response(status=status.HTTP_400_BAD_REQUEST, data=error)

		if len(already_invited) > 0:
			error = {
				"already_invited": already_invited
			}
			return Response(status=status.HTTP_200_OK, data=error)

		return Response(status=status.HTTP_201_CREATED)

	def delete(self, request, invite_id):
		invite = get_object_or_404(Invite, id=invite_id)
		invite.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)


class AcceptInviteView(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, invite_id):
		invite = get_object_or_404(Invite, id=invite_id, status="pending")
		invite.status = "accepted"
		invite.save()

		return Response(status=status.HTTP_200_OK)


class DeclineInviteView(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request, invite_id):
		invite = get_object_or_404(Invite, id=invite_id, status="pending")
		invite.status = "declined"
		invite.save()

		return Response(status=status.HTTP_200_OK)


class SuggestionView(APIView):

	# you get suggestions when GET-ing the Event, so this get function might not be needed
	def get(self, request, event_id):
		suggestions = Suggestion.objects.filter(event=event_id)
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
		user_instance.set_password(request.data.get("password"))
		user_instance.save()
		# user_instance.profile.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AliasGetToken(APIView):

	@csrf_exempt
	def post(self, request):
		alias = request.data.get("alias")
		user, created = User.objects.get_or_create(username=alias)
		user.set_unusable_password()
		user.save()

		# by this point, made a new user
		# return token to client

		serializer = TokenSerializer(user.auth_token)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
