#============================= CORE IMPORTS =============================#
from __future__ import unicode_literals

#============================ DJANGO IMPORTS ============================#
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

#======================== REST FRAMEWORK IMPORTS ========================#
from rest_framework.authtoken.models import Token

# Create your models here.

class Event(models.Model):
	title = models.CharField(max_length=100, default="No title")
	creator = models.ForeignKey(User, related_name="events_created", null=True)
	location = models.CharField(max_length=303)
	time = models.CharField(max_length=404)
	activity = models.CharField(max_length=330)

	def get_attendees(self):
		attendees = self.invite_set.filter(status="accepted")
		return attendees

	def get_invitees(self):
		attendees = self.invite_set.filter(status="pending")
		return attendees

	def get_declined_invites(self):
		attendees = self.invite_set.filter(status="declined")
		return attendees

	def __str__(self):
		return "%s @ %s @ %s" % (self.activity, self.time, self.location)

class Suggestion(models.Model):
	user = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	location = models.CharField(max_length=303)
	time = models.CharField(max_length=404)
	activity = models.CharField(max_length=330)

	def __str__(self):
		return "%s @ %s @ %s" % (self.activity, self.time, self.location)

class Invite(models.Model):
	event = models.ForeignKey(Event)
	user = models.ForeignKey(User)
	status = models.CharField(max_length=50, default="pending")


#=============================== SIGNALS ================================#

# This is most likely a signal receiver that runs the function whenever a new User is created
# It creates a new Token and Profile and associated it with the created User.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)



"""
What we wanna do here is to create a pre_save signal where when an Event is
saved, it autoassigns the event's creator attribute to the logged in user
"""

# @receiver(pre_save, sender=Event)
# def set_event_creator(sender, instance=None, **kwargs):
	
