from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers.common import BasketSerializer
from .models import Basket
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrShared
from .serializers.populate import PopulatedBasketSerializer

# Create your views here.
class BasketsView (APIView): 
    permission_classes =[IsAuthenticated]
    
    #Index all baskets
    def get (self, request):
        baskets = Basket.objects.all()
        serializer = BasketSerializer (baskets, many=True)
        return Response (serializer.data)

    #Create a new basket
    def post (self, request): 
        request.data ['owner'] = request.user.id
        serializer = BasketSerializer (data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response (serializer.data, status=201)


class BasketUserView(APIView):
    permission_classes =[IsAuthenticated]
    
    #Index the baskets of a specific owner
    def get (self, request):  
        baskets_owned = Basket.objects.filter(owner=request.user.id)
        baskets_shared = Basket.objects.filter (shared_with=request.user.id)
        baskets = (baskets_owned | baskets_shared).distinct()
        serializer = PopulatedBasketSerializer (baskets, many=True)
        return Response (serializer.data, status=201)


class BasketsDetailsView(APIView):
    permission_classes = [IsOwnerOrShared]    
    
    def get_object (self, pk): 
        try: 
           return Basket.objects.get (pk=pk)
        except Basket.DoesNotExist: 
            raise NotFound (detail = 'Basket is no longer available')
    
    def get (self, request, pk):
        basket = self.get_object(pk)
        self.check_object_permissions(request, basket)
        serializer =PopulatedBasketSerializer(basket)
        return Response (serializer.data)
    
    def put (self, request, pk):      
        basket = self.get_object (pk)
        self.check_object_permissions(request, basket)
        serializer = BasketSerializer(basket, data= request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response (serializer.data)
        
    def delete (self, request, pk):
        basket= self.get_object (pk)
        self.check_object_permissions(request, basket)
        basket.delete()
        return Response (status = 204)