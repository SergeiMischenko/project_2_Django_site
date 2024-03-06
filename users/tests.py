from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterUserTestCase(TestCase):
    def setUp(self):
        pass

    def test_form_registration_get(self):
        path = reverse("users:register")
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register.html")
