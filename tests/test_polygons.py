from django.urls import reverse
from locations.models import Coordinate, Polygon, Provider
from rest_framework import status
from rest_framework.test import APITestCase


class ProviderTests(APITestCase):
    def setUp(self):
        self.user_data1 = {
            "username": "auth_test_user",
            "email": "test_user@moziogroup.hr",
            "password": "testingapis123",
            "first_name": "Auth Test",
            "last_name": "User",
            "phone_number": "123456789",
        }

        self.auth_user = Provider.objects.create(**self.user_data1)
        self.user_data2 = {
            "username": "test_user",
            "email": "test_user@moziogroup.hr",
            "password": "testingapis123",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "123456789",
        }
        self.user = Provider.objects.create(**self.user_data2)
        self.coordinate_data = {"latitude": 9999.1, "longitude": 200.2}
        self.coordinate = Coordinate.objects.create(**self.coordinate_data)
        self.polygon_data = {
            "name": "Fake Polygon",
            "price": 10000.99,
        }
        self.polygon = Polygon.objects.create(
            provider=self.auth_user, **self.polygon_data
        )
        self.polygon.coordinates.add(self.coordinate)

    def test_does_not_allow_unauthenticated_users_access_the_endpoints(self):
        list_providers = self.client.get(reverse("polygons-list"), format="json")
        providers_detail = self.client.put(
            reverse("polygons-detail", args=[1]), self.user_data1, format="json"
        )
        self.assertEqual(list_providers.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(providers_detail.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_polygons_list_is_succesfully_returned(self):
        url = reverse("polygons-list")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_polygon_by_id_works_as_expected_and_returns_correct_polygon(self):
        url = reverse(
            "polygons-detail",
            args=[
                1,
            ],
        )
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_polygon_by_id_returns_appropriate_response_once_polygon_is_not_found(
        self,
    ):
        url = reverse(
            "polygons-detail",
            args=[
                11,
            ],
        )
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_polygons_update_works_as_expected_and_updates_polygon(self):
        self.polygon_data["name"] = "Changed Name"
        url = reverse(
            "polygons-detail",
            args=[
                1,
            ],
        )
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, self.polygon_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_get_polygon_update_works_as_expected_and_returns_appropriate_error_when_polygon_does_not_exist(
        self,
    ):
        url = reverse("polygons-detail", args=[20])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, self.polygon_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_polygon_detail_is_succesfully_destroyed(self):
        url = reverse("polygons-detail", args=[1])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_polygon_detail_cannot_be_destroyed_by_who_didnt_create_it(self):
        url = reverse("polygons-detail", args=[1])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_polygon_works_as_expected_and_returns_appropriate_error_when_polygon_does_not_exist(
        self,
    ):
        url = reverse("polygons-detail", args=[10])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_find_by_coordinates_returns_appropriate_response(self):
        url = reverse("polygons-coordinates")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, self.coordinate_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_find_by_coordinates_returns_appropriate_response_when_coordinates_dont_exist(
        self,
    ):
        url = reverse("polygons-coordinates")
        self.client.force_authenticate(user=self.auth_user)
        self.coordinate_data["latitude"] = 2202.22
        response = self.client.post(url, self.coordinate_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
