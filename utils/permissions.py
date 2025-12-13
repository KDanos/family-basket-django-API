from rest_framework.permissions import BasePermission
from baskets.models import Basket

class IsOwnerOrShared (BasePermission):
    def has_object_permission(self, request, view, basket):
        if request.method == 'DELETE': 
            return request.user == basket.owner
        return request.user in basket.shared_with.all() or request.user == basket.owner

class HasBasketPermission (BasePermission): 
    def has_permission (self, request, view):
        basket_pk = view.kwargs.get('pk')
        print ('===========You are inside the BasketPermission class========================')
        print (f'the basket pk is {basket_pk}')
        print ('============================================================================')

        try: 
            basket = Basket.objects.get(pk=basket_pk)
            is_owner = basket.owner==request.user
            is_shared = request.user in basket.shared_with.all()
            return is_owner or is_shared
        except Basket.DoesNotExist:
            return False

        
        