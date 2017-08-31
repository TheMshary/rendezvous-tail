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

#============================== API TESTS ===============================#

# class SearchTest(APITestCase):

# 	def setUp(self):
# 		info = [
# 			('a', 'a', 1.0, 'pet'),
# 			('b', 'b', 2.0, 'cleaning'),
# 			('c', 'c', 2.5, 'real estate'),
# 			('d', 'd', 3.5, 'pet')
# 		]

# 		# make 3 Provider accounts
# 		for inf in info:
# 			user = User.objects.create_user(username=inf[0], password=inf[1])
# 			user.profile.usertype = 'provider'
# 			user.profile.category = inf[3]
# 			user.profile.rating.rate = inf[2]
# 			user.profile.rating.save()
# 			user.profile.save()

# 		# login
# 		token = Token.objects.get(user__username='a')
# 		# Include an appropriate 'Authorization:' header on all requests.
# 		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

# 	def test_search(self):	#documented
# 		url = '/search/'
# 		data = {
# 			'search':'pet',
# 		}
# 		response = self.client.post(url, data, format='json')

# 		# self.assertTrue(isinstance(response.data.get(''), Profile))
# 		self.assertEqual(response.status_code, status.HTTP_200_OK)