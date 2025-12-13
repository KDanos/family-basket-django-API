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

#Index of all users, only available after sign-in
class UserView (APIView):
    permission_classes = [IsAuthenticated]
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

    #Show personal details, with populated connections
    def get(self, request, pk): 
        user = self.get_user(pk)
        #Can this authorisation be automated?
        if request.user != user:
            raise PermissionDenied
        serializer = PopulatedUserSerializer (user)
        return Response (serializer.data)
    
    #Edit personal details, only availbale after sign and authorised
    def put (self, request, pk):
        user = self.get_user (pk)
        #Can this authorisation be automated?
        if request.user != user: 
            raise PermissionDenied
        serializer=UserSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response (serializer.data)

    #Delete account completely
    def delete (self, request, pk):
        user = self.get_user (pk)
        #Can this authorisation be automated?
        if request.user !=user:
            raise PermissionDenied
        user.delete()
        return Response (status = 204)

class UpdatePasswordView(APIView):
    #Reset password
    def get_user (self, username):
        try: 
            return User.objects.get (username=username)
        except User.DoesNotExist:
            raise NotFound (detail= 'User is no longer available')    
    
    def patch (self, request, username):
        user = self.get_user(username)
        try:
            print ('found user', user)
            new_password=123
            user.set_password (str(new_password))
            user.save()
            return Response ({'message' : f'Updated the password for user {username } to {str(new_password)}'},status=200)
        except: 
            raise NotFound (detail= f'Could not update the password for user{username}')
        
