from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from baskets.models import Basket
from items.serializers.populated import PopulatedItemSerializer
from .models import Item
from .serializers.common import ItemSerializer
from rest_framework.exceptions import NotFound
from utils.permissions import HasBasketPermission, HasItemPermission

# Create your views here.
class ItemsView(APIView): 
    permission_classes = [IsAuthenticated , HasBasketPermission]
    
    def get_basket (self, pk): 
        try: 
            return Basket.objects.get (pk=pk)
        except: 
            raise NotFound

    #Index all the items of a specific basket
    def get (self, request ,pk): 
        items = Item.objects.filter(basket=pk)
        serializer= ItemSerializer(items, many = True)  
        return Response (serializer.data)

    #Create a new item
    def post (self, request, pk):   
        request.data['basket'] =  basket =  self.get_basket(pk).id
        request.data['creator'] = request.user.id
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response (serializer.data, status=201)

class ItemsDetaiView(APIView):
    permission_classes =[IsAuthenticated, HasItemPermission]
    
    def get_item (self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise NotFound(detail = 'Item is no longer available')

    #Show single item
    def get (self, request, pk):
        item= self.get_item(pk)
        serializer = ItemSerializer (item)
        return Response(serializer.data ) 

    #Edit a single item
    def put (self, request, pk):
        item = self.get_item (pk)
        serializer = ItemSerializer (item, data=request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response (serializer.data)

    #Delete a single item
    def delete (self, request, pk):
        item = self.get_item(pk)
        item.delete()
        return Response (status = 204)