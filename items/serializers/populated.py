from .common import ItemSerializer
from baskets.serializers.common import BasketSerializer
from users.serializers.common import UserSerializer

class PopulatedItemSerializer (ItemSerializer):
    basket = BasketSerializer()
    creator = UserSerializer()