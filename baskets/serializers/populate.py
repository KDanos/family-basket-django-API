from .common import BasketSerializer
from users.serializers.common import UserSerializer

class PopulatedBasketSerializer (BasketSerializer):
    shared_with = UserSerializer(many=True)