from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Income, Expenditure
from decimal import Decimal

class UserTests(APITestCase):

    def setUp(self):
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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data) 
        self.assertIsInstance(response.data['token'], str)  
        self.assertGreater(len(response.data['token']), 0)  

        # Saving the token for later use in the other tests
        self.token = response.data['token']

    def test_login(self):
        self.assertIsNotNone(self.token)  

    def test_logout(self):
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url)

        # Checks if logout is successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_profile(self):
        url = reverse('user-profile', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)

        # Checks if user profile is retrieved correctly
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
          'user': self.user.id,  
          'title': 'Salary',
          'amount': '500.00',  
          'description': 'Salary for November,'
        }
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
      response = self.client.post(url, data, format='json')

      # Checks if income is created successfully
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(response.data['title'], 'Salary')
      self.assertEqual(response.data['amount'], '500.00')
      self.assertEqual(response.data['description'], 'Salary for November,')



    def test_income_detail(self):
        income = Income.objects.create(user=self.user, amount=Decimal('500.00'), description='Salary')
        url = reverse('income-detail', kwargs={'pk': income.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)

        # Checks if correct income detail is retrieved
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
        url = reverse('expenditure-list') 
        data = {
            'title': 'Groceries',
            'amount': '100.00',
            'date': '2024-11-25',
            'description': 'Monthly grocery shopping'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        # Checks if expenditure is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Groceries')
        self.assertEqual(response.data['amount'], '100.00')

    def test_expenditure_detail(self):
        expenditure = Expenditure.objects.create(user=self.user, title='Groceries', amount=Decimal('100.00'), date='2024-11-25', description='Monthly grocery shopping')
        url = reverse('expenditure-detail', kwargs={'pk': expenditure.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)

        # Checks if correct expenditure detail is retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Groceries')
        self.assertEqual(response.data['amount'], '100.00')
