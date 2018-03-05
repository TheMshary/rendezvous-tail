#============================ Django IMPORTS ==============================#
from django.contrib.auth.models import User

#======================== REST FRAMEWORK IMPORTS ========================#
from rest_framework import serializers
from rest_framework.authtoken.models import Token

#============================= APP IMPORTS ==============================#
from app.models import Event, Suggestion, Invite

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username',)

class TokenSerializer(serializers.ModelSerializer):
	class Meta:
		model = Token
		fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
	attendees = UserSerializer(read_only=True, many=True)

	class Meta:
		model = Event
		fields = '__all__'


class SuggestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Suggestion
		fields = '__all__'


class InviteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Invite
		fields = '__all__'

	def to_representation(self, instance):
		data = super(InviteSerializer, self).to_representation(instance)
		data.update({
			"username": instance.user.username
			})
		return data
