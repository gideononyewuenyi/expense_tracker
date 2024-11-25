from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Income, Expenditure
from decimal import Decimal

class UserTests(APITestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username="testuser", password="testpassword123")
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        login_response = self.client.post(url, data, format='json')
        self.token = login_response.data['token']

    def test_signup(self):
        url = reverse('signup')
        data = {
            "username": "testuser2",
            "password": "testpassword123",
            "email": "testuser2@example.com"
        }
        response = self.client.post(url, data, format='json')

        # Check if user is created and token is returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)  # Ensure token is returned
        self.assertIsInstance(response.data['token'], str)  # Token should be a string
        self.assertGreater(len(response.data['token']), 0)  # Token should not be empty

        # Save the token for later use in other tests
        self.token = response.data['token']

    def test_login(self):
        # Login logic already in setUp
        self.assertIsNotNone(self.token)  # Ensure that token is set

    def test_logout(self):
        url = reverse('logout')
        # Add the token to the request header for logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url)

        # Check if logout is successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_profile(self):
        # Ensure the correct userID is passed to reverse() for user profile
        url = reverse('user-profile', kwargs={'pk': self.user.pk})
        # Add the token to the request header for the user profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)

        # Check if user profile is retrieved correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)


class IncomeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword123")
        self.client.login(username="testuser", password="testpassword123")

        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        login_response = self.client.post(url, data, format='json')
        self.token = login_response.data['token']


    def test_income_list_create(self):
      url = reverse('income-list')
      data = {
          'user': self.user.id,  # Ensure the user field is included
          'title': 'Salary',
          'amount': '500.00',  # Ensure it's a string that can be converted to Decimal
          'description': 'Salary for November,'
        }
      # Add the token to the request header for income creation
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
      response = self.client.post(url, data, format='json')

      # Check if income is created successfully
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(response.data['title'], 'Salary')
      self.assertEqual(response.data['amount'], '500.00')
      self.assertEqual(response.data['description'], 'Salary for November,')



    def test_income_detail(self):
        income = Income.objects.create(user=self.user, amount=Decimal('500.00'), description='Salary')
        url = reverse('income-detail', kwargs={'pk': income.pk})
        # Add the token to the request header for income details
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)

        # Check if correct income detail is retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '500.00')
        self.assertEqual(response.data['description'], 'Salary')


class ExpenditureTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword123")
        self.client.login(username="testuser", password="testpassword123")

        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        login_response = self.client.post(url, data, format='json')
        self.token = login_response.data['token']

    def test_expenditure_list_create(self):
        url = reverse('expenditure-list')  # Updated URL name here
        data = {
            'title': 'Groceries',
            'amount': '100.00',
            'date': '2024-11-25',
            'description': 'Monthly grocery shopping'
        }
        # Add the token to the request header for expenditure creation
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        # Check if expenditure is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Groceries')
        self.assertEqual(response.data['amount'], '100.00')

    def test_expenditure_detail(self):
        expenditure = Expenditure.objects.create(user=self.user, title='Groceries', amount=Decimal('100.00'), date='2024-11-25', description='Monthly grocery shopping')
        url = reverse('expenditure-detail', kwargs={'pk': expenditure.pk})
        # Add the token to the request header for expenditure details
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)

        # Check if correct expenditure detail is retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Groceries')
        self.assertEqual(response.data['amount'], '100.00')
