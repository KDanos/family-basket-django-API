from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers.common import BasketSerializer
from .models import Basket
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class HelloWorldView (APIView):
    def get (self, request):
        return Response ({'message': 'Hello, world!'})

class BasketsView (APIView): 
    permission_classes =[IsAuthenticated]
    
    def get (self, request):
        baskets = Basket.objects.all()
        serializer = BasketSerializer (baskets, many=True)
        return Response (serializer.data)

    def post (self, request): 
        request.data ['owner'] = request.user.id
        serializer = BasketSerializer (data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response (serializer.data, status=201)

class BasketsDetailsView(APIView):
    
    def get_object (self, pk): 
        try: 
           return Basket.objects.get (pk=pk)
        except Basket.DoesNotExist: 
            raise NotFound (detail = 'Basket is no longer available')
    
    def get (self, request, pk):
        basket = self.get_object(pk)
        serializer = BasketSerializer(basket)
        return Response (serializer.data)
    
    def put (self, request, pk):
        basket = self.get_object (pk)
        serializer = BasketSerializer(basket, data= request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response (serializer.data)
        
    def delete (self, request, pk):
        basket = self.get_object(pk)
        basket.delete()
        return Response (status = 204)