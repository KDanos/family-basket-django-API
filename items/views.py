from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from baskets.models import Basket
from items.serializers.populated import PopulatedItemSerializer
from .models import Item
from .serializers.common import ItemSerializer
from rest_framework.exceptions import NotFound
from utils.permissions import HasBasketPermission

# Create your views here.
class ItemsView(APIView): 
    permission_classes = [IsAuthenticated , HasBasketPermission]
    
    def get_basket (self, pk): 
        try: 
            return Basket.objects.get (pk=pk)
        except: 
            raise NotFound

    def get (self, request ,pk): 
        # basket = self.get_basket(pk)
        items = Item.objects.filter(basket=pk)
        serializer= ItemSerializer(items, many = True)  
        return Response (serializer.data)

    def post (self, request, pk):   
        request.data['basket'] =  basket =  self.get_basket(pk).id
        request.data['creator'] = request.user.id
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response (serializer.data, status=201)