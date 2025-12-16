from django.urls import path
from .views import BasketsView , BasketsDetailsView, BasketUserView
from items.views import ItemsView


urlpatterns = [
    path('new/', BasketsView.as_view()),    
    path('', BasketUserView.as_view()), 
    path ('<int:pk>/items/',ItemsView.as_view() ),
    path ('<int:pk>/',BasketsDetailsView.as_view())
]