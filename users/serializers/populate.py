from .common import UserSerializer

class PopulatedUserSerializer (UserSerializer):
    connections = UserSerializer(many=True)