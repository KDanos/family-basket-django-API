from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from .serializers.common import UserSerializer


# Create your views here.
class SignUpView (APIView): 
    def post (self, request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response ({'message':'User created successfully!'})

class UserView (APIView):
    def get (self, request):
        allUsers = User.objects.all()
        serializer = UserSerializer(allUsers, many=True)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response (serializer.data, status=201)


