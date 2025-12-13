from django.urls import path 
from .views import ItemsView, ItemsDetaiView

urlpatterns = [
    path('<int:pk>/', ItemsDetaiView.as_view())
]