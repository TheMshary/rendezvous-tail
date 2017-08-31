from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from model_mommy import mommy

from app.models import *

# Create your tests here.

#======================== API TESTS ========================#

class EventTest(APITestCase):
	pk = None

	def setUp(self):
		self.pk = mommy.make(Event, _quantity=3)[0].pk

	def test_get_list(self):
		url = '/event/'
		response = self.client.get(url, format='json')

		count = len(response.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(count, 3)

	def test_get(self):
		url = '/event/'
		data = {
			'pk': self.pk
		}
		response = self.client.get(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# self.assertEqual(response.data.get('pk'), self.pk)
		print response.data


#======================== MODEL TESTS ========================#

# class ProfileTest(TestCase):
# 	profile = None

# 	def setUp(self, username="tsty", password="psst"):
# 		self.profile = User.objects.create_user(username=username, password=password).profile

# 	def test_whatever_creation(self):
# 		w = self.profile
# 		self.assertTrue(isinstance(w, Profile))
# 		self.assertEqual(w.__unicode__(), w.user.username)

#======================== SERIALIZER TESTS ========================#

# from app.serializers import *

# class OfferedServiceSerializerModelTest(TestCase):
# 	def test_valid_and_update(self):
# 		serv = mommy.make(Service)
# 		w = mommy.make(OfferedService, service=serv)
# 		data = {
# 			'service': {
# 				'title': w.service.title,
# 				'description': w.service.description,
# 				'price': w.service.price,
# 			},
# 		}
# 		serializer = OfferedServiceSerializer(data=data)
# 		self.assertTrue(serializer.is_valid())
# 		saved = serializer.save()
# 		self.assertTrue(isinstance(saved, OfferedService))

# 		# update
# 		data.update({
# 			'service': {
# 				'title': 'new title',
# 			},
# 		})
# 		serializer = OfferedServiceSerializer(saved, data=data)
# 		self.assertTrue(serializer.is_valid())
# 		saved = serializer.save()
# 		self.assertTrue(isinstance(saved, OfferedService))

# 	def test_invalid(self):
# 		serv = mommy.make(Service)
# 		w = mommy.make(OfferedService, service=serv)
# 		data = {
# 			'service': {
# 				'title': w.service.title,
# 				'description': '',
# 				'price': '',
# 			},
# 		}
# 		serializer = OfferedServiceSerializer(data=data)
# 		self.assertFalse(serializer.is_valid())
