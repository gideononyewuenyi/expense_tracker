from django.urls import path
from .views import (
    SignupView, LoginView, LogoutView, UserProfileView,
    IncomeListView, IncomeDetailView, ExpenditureListCreateView, ExpenditureDetailView
)

urlpatterns = [
    # User-related endpoints
    path('auth/signup', SignupView.as_view(), name='signup'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/user/<int:pk>/profile', UserProfileView.as_view(), name='user-profile'),

    # Income-related endpoints
    path('user/income', IncomeListView.as_view(), name='income-list'),
    path('user/income/<int:pk>', IncomeDetailView.as_view(), name='income-detail'),

    # Expenditure-related endpoints
    path('user/expenditure', ExpenditureListCreateView.as_view(), name='expenditure-list'),
    path('user/expenditure/<int:pk>', ExpenditureDetailView.as_view(), name='expenditure-detail'),
]

