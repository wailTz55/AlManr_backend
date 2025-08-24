from . import views
from django.urls import path
# from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('activities/', views.get_activities, name='activities'),
    path('all-data/', views.get_all_data, name='all_data'),
    path("registration/", views.ApplicationView.as_view(), name="registration"),


]
