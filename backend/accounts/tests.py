from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsTestCase(APITestCase):
    """Test cases for `accounts` application."""

    register_url = "/api/auth/register/"
    verify_email_url = "/api/auth/register/verify-email/"
    login_url = "/api/auth/login/"

    def test_registration(self):
        """
        Test email registration with POST request and dummy payload. All code
        must be put under a single unit test for the entire registration process.
        """
        data = {
            "email": "example-user@example-email.com",
            "password1": "secretPassword",
            "password2": "secretPassword",
        }

        # send POST request with `data` payload to "/api/auth/register/"
        response = self.client.post(self.register_url, data)

        # check the response status and data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["detail"], "Verification e-mail sent.")

        # log in with the registered credentials before verification
        login_data = {
            "email": data["email"],
            "password": data["password1"],
        }
        response = self.client.post(self.login_url, login_data)

        # logging into an unverified email fails with code 400 bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            "E-mail is not verified." in response.json()["non_field_errors"]
        )

        # expect one email to be sent; parse that email to get verification token
        self.assertEqual(len(mail.outbox), 1)
        email_lines = mail.outbox[0].body.splitlines()

        # "To confirm this is correct, go to http://testserver/verify-email/{key}/"
        verification_line = [ln for ln in email_lines if "verify-email" in ln][0]
        verification_link = verification_line.split("go to ")[-1]
        verification_key = verification_link.split("/")[-2]

        # verify email by going to verification url and POSTing verification key
        response = self.client.post(self.verify_email_url, {"key": verification_key})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["detail"], "ok")

        # log in again after verifying the email; receive key in response
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("key" in response.json())
