from .common import BasketSerializer
from users.serializers.common import UserSerializer
from items.serializers.common import ItemSerializer

class PopulatedBasketSerializer (BasketSerializer):
    shared_with = UserSerializer(many=True)
    basket_items = ItemSerializer (many= True)