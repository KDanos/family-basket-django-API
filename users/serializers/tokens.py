from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)

        #Add custom claims
        token ['user']= {
            'id': user.id,
            'username': user.username,
            'profile_image': user.profile_image
        }
        return token