from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated


from users.models import User
from .serializers.common import UserSerializer
from .serializers.populate import PopulatedUserSerializer


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
        return Response (serializer.data, status=201)

class UserDetailView (APIView): 
    permission_classes = [IsAuthenticated]
    
    def get_user (self, pk):
        try: 
            return User.objects.get (pk=pk)
        except User.DoesNotExist:
            raise NotFound (detail= 'User is no longer available')

    def get(self, request, pk): 
        user = self.get_user(pk)
        if request.user != user:
            raise PermissionDenied
        serializer = PopulatedUserSerializer (user)
        return Response (serializer.data)

    def put (self, request, pk):
        user = self.get_user (pk)
        if request.user != user: 
            raise PermissionDenied
        serializer=UserSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response (serializer.data)
