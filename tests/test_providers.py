from django.urls import reverse
from locations.models import Provider
from rest_framework import status
from rest_framework.test import APITestCase


class ProviderTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "test_user",
            "email": "test_user@moziogroup.hr",
            "password": "testingapis123",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "123456789",
        }

        self.auth_user = Provider.objects.create(**self.user_data)

    def test_providers_list_is_succesfully_returned(self):
        url = reverse("providers-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_provider_by_id_works_as_expected_and_returns_user(self):
        url = reverse(
            "providers-detail",
            args=[
                1,
            ],
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_provider_by_id_returns_appropriate_response_once_provider_is_not_found(
        self,
    ):
        url = reverse(
            "providers-detail",
            args=[
                11,
            ],
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_provider_update_works_as_expected_and_updates_user(self):
        self.user_data["username"] = "ChangedName"
        url = reverse(
            "providers-detail",
            args=[
                1,
            ],
        )
        response = self.client.put(url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_get_provider_update_works_as_expected_and_returns_appropriate_error_when_provider_does_not_exist(
        self,
    ):
        url = reverse("providers-detail", args=[20])
        response = self.client.put(url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_providers_detail_is_succesfully_destroyed(self):
        url = reverse("providers-detail", args=[1])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_provider_works_as_expected_and_returns_appropriate_error_when_provider_does_not_exist(
        self,
    ):
        url = reverse("providers-detail", args=[10])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_providers_login_successfully(self):
        url = reverse("providers-login")
        login_request = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(url, login_request, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_works_as_expected(self):
        url = reverse("providers-logout")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_only_authorized_users(self):
        url = reverse("providers-logout")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
