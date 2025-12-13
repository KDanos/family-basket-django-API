from django.urls import path
from .views import BasketsView , BasketsDetailsView
from items.views import ItemsView


urlpatterns = [
    path('', BasketsView.as_view()),    
    path ('<int:pk>/items/',ItemsView.as_view() ),
    path ('<int:pk>/',BasketsDetailsView.as_view())
]