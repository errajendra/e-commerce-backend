from django.test import TestCase

from rest_framework.test import APITestCase, APIClient
# from unit_test.BaseTestCase import BaseTestCase
from unit_test.test_response_message import verify_api_response, write_test_result
from unit_test.api_url import *
from rest_framework import status
from unit_test.test_payload_data import *

'''
Author:bhawna
Date:05/01/2024
Note: Test Module for akshra weekly challenge list and detail api. 
'''
class WeeklyChallengeListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # self.client.force_authenticate(user=self.user)
         
    def test_get_contry_code_list(self):
        url = COUNTRY_CODE_URL
        try:
            response = self.client.get(url, format='json')
            verify_api_response(response, status, "User API", url, response.data, self, response.data)
        except Exception as error:
            write_test_result("API", url, "FAILED", str(error), 400)

    
    def test_register_user(self):
        # page = json_weekly_challenges_api.get('page', None)
        url = REGISTER_USER_URL
        try:
            response = self.client.post(url, json_user_register, format="json")
            verify_api_response(response, status, "API", url, response.data['message'], self, response.data)
        except Exception as error:
            self.assertFalse(False)
            write_test_result("API", url, "FAILED", str(error), 400)


