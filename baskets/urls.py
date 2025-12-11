from django.urls import path
from .views import HelloWorldView, BasketsView , BasketsDetailsView



urlpatterns = [
    path('hello/', HelloWorldView.as_view()),
    path('', BasketsView.as_view()),    
    path ('<int:pk>/',BasketsDetailsView.as_view() )
]