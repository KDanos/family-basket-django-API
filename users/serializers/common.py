from rest_framework import serializers
from ..models import User
from django.contrib.auth import password_validation, hashers

class UserSerializer (serializers.ModelSerializer): 
    password = serializers.CharField (write_only= True)
    confirm_password = serializers.CharField(write_only = True)
    
    class Meta: 
        model = User
        fields = [
            'id', 
            'username',
            'email', 
            'password', 
            'confirm_password',
            'profile_image',
            'connections',
            'is_staff'
        ]

    def validate (self, data):
        password = data.get ('password')
        confirm_password = data.pop ('confirm_password',None) #None makes sure that an empty confirm_password entry does not raise an exception
        
        #Check that the passwords match
        if password != confirm_password:
            raise serializers.ValidationError ({
                'confirm_password': 'Passwords do not match.'
            })
        #Use django's built-in password validation (under 'AUTH_PASSWORD_VALIDATORS' in settings.py)
        # password_validation.validate_password(password)
        #Hash the password before saving
        data['password']=hashers.make_password(password)
        return data