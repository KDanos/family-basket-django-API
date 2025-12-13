from rest_framework.permissions import BasePermission
from baskets.models import Basket
from items.models import Item

class IsOwnerOrShared (BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE': 
            return request.user == obj.owner
        return request.user in obj.shared_with.all() or request.user == obj.owner

class HasBasketPermission (BasePermission): 
    def has_permission (self, request, view):
        basket_pk = view.kwargs.get('pk')
        try: 
            basket = Basket.objects.get(pk=basket_pk)
            is_owner = basket.owner==request.user
            is_shared = request.user in basket.shared_with.all()
            return is_owner or is_shared
        except Basket.DoesNotExist:
            return False

class HasItemPermission (BasePermission):
    def has_permission (self, request, view):
        item_pk = view.kwargs.get('pk')
        try: 
            item = Item.objects.get(pk = item_pk)
            is_basket_owner =item.basket.owner == request.user
            is_basket_shared = request.user in item.basket.shared_with.all()
            return is_basket_owner or is_basket_shared
        except Item.DoesNotExist: 
            return False
        