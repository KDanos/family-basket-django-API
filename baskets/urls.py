from django.urls import path
from .views import HelloWorldView, BasketsView , BasketsDetailsView
from items.views import ItemsView


urlpatterns = [
    path('hello/', HelloWorldView.as_view()),
    path('', BasketsView.as_view()),    
    path ('<int:pk>/items/',ItemsView.as_view() ),
    path ('<int:pk>/',BasketsDetailsView.as_view() )
]