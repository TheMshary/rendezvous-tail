#============================ Django IMPORTS ==============================#
from django.contrib.auth.models import User

#======================== REST FRAMEWORK IMPORTS ========================#
from rest_framework import serializers
from rest_framework.authtoken.models import Token

#============================= APP IMPORTS ==============================#
from app.models import Event, Suggestion


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = '__all__'


class SuggestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Suggestion
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'password')

