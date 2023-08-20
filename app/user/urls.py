"""
URL mappings for the user API.
"""
from django.urls import path

from user import views

# Will be used for the revers-mapping, that defined \
# in test_user_api.py \
# (line: "CREATE_USER_URL = reverse('user:create')")
app_name = 'user'
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
