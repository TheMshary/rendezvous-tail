#============================ DJANGO IMPORTS ============================#
from django.test import TestCase
from django.contrib.auth.models import User

#======================== REST FRAMEWORK IMPORTS ========================#
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

#============================= APP IMPORTS ==============================#
from app.models import *
from app.serializers import OfferedServiceSerializer

from model_mommy import mommy

#============================= MODEL TESTS ==============================#


# class EventTest(TestCase):
# 	profile = None

# 	def setUp(self, username="tsty", password="psst"):
# 		self.profile = User.objects.create_user(username=username, password=password).profile

# 	def test_creator_assignment(self):
# 		w = self.profile
# 		self.assertTrue(isinstance(w, Profile))
# 		self.assertEqual(w.__unicode__(), w.user.username)
