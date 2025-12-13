from django.urls import path
from .views import SignUpView, UserView, UserDetailView, UpdatePasswordView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path ('', UserView.as_view()),
    path ('sign-up/', SignUpView.as_view()),
    path ('sign-in/', TokenObtainPairView.as_view()),
    path ('<int:pk>/', UserDetailView.as_view()),
    path('password-reset/<str:username>/', UpdatePasswordView.as_view())
]