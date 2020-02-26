from django.test import TestCase
from django.test import Client
from django.urls import reverse
from unittest.mock import MagicMock
from unittest.mock import patch
from decimal import Decimal

import json

from .models import User, Address, Answer
from .tasks import fetch_location

example_post_OK = {
	"user_info": {
		"phone": "(11) 98765-4321",
		"name": "João da Silva",
		"email": "joao_silva@exemplo.com"
	},
	"address_attributes": {
		"city": "São Paulo",
		"neighborhood": "Jardim Paulista",
		"street": "Avenida São Gabriel",
		"uf": "SP",
		"zip_code": "01435-001"
	},
	"request_info": {
		"question1": "answer1",
		"question2": "answer2",
		"question3": "answer3"
	}
}

class UserAddressViewTest(TestCase):

	def setUp(self):
		self.client = Client()

	@patch("postHandler.tasks.fetch_location.delay")
	def test_post_OK_request(self, mock_location_fetcher_task):
		'''
		If a post request is made, save user, address and answer data to database
		and create a celery task to retrieve that address location data.
		'''

		# Send the post request:
		response = self.client.post(
			reverse('add_user_address'), json.dumps(example_post_OK), content_type='application/json')

		# Check if the response is correct:
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "User information added.")

		# Check if user was created in the database:
		created_user = User.objects.get(name_text="João da Silva")
		self.assertEqual(created_user.email_text, 'joao_silva@exemplo.com')
		self.assertEqual(created_user.phone_text, '(11) 98765-4321')

		#Check if address was created in the database:
		created_address = created_user.address_set.get(city_text='São Paulo')
		self.assertEqual(created_address.neighborhood_text, "Jardim Paulista")
		self.assertEqual(created_address.street_text, "Avenida São Gabriel")
		self.assertEqual(created_address.uf_code, "SP")
		self.assertEqual(created_address.zip_code, "01435-001")

		#Check if answers were created:
		created_answer_1 = created_user.answer_set.get(answer_text='answer1')
		self.assertEqual(created_answer_1.question_text, "question1")
		created_answer_2 = created_user.answer_set.get(answer_text='answer2')
		self.assertEqual(created_answer_2.question_text, "question2")
		created_answer_3 = created_user.answer_set.get(answer_text='answer3')
		self.assertEqual(created_answer_3.question_text, "question3")

		#Check if location fetcher task was called:
		mock_location_fetcher_task.assert_called_with(address_id=created_address.id, street="Avenida São Gabriel", city="São Paulo", state="SP")

	# TODO: Add more tests, including exception occurring tests.
		# IDEA: get request.
		# IDEA: post request with missing info.
		# IDEA: post request with wrong info (city that doesn't exist).
		# IDEA: post request for already present user.

class FetchLocationTaskTest(TestCase):

	@patch('postHandler.tasks.google_client.geocode')
	def test_fetch_example_location(self, mocked_geocode):
		mocked_geocode.return_value = [{"geometry": {"location": {"lat": 12.345678,"lng": 87.654321}}}]

		# Create address to update in the database
		created_user = User(name_text="João da Silva")
		created_user.save()
		created_address = created_user.address_set.create(city_text="São Paulo")
		created_address.save()

		# Emit the task:
		location_result = fetch_location(address_id=created_address.id, street="Avenida São Gabriel", city="São Paulo", state="SP")

		# Check if the google API was called:
		mocked_geocode.assert_called_with("Avenida São Gabriel, São Paulo, SP")

		# Check if the address was updated:
		created_address.refresh_from_db()
		self.assertEqual(created_address.latitude, Decimal("12.345678"))
		self.assertEqual(created_address.longitude, Decimal("87.654321"))
