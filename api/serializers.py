from rest_framework import serializers
from account.models import User ,  Profile 
from .models import *
from rest_framework import status
from product.models import Product ,ProductImage, ProductCategory , Company
from multiprocessing import AuthenticationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str , force_str , smart_bytes , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name','last_name', 'address', 'phone_number' , 'profile_image' ]
    
 
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    

    class Meta:
        model = User
        fields = ['slug','username', 'email', 'profile']
        extra_kwargs = {
            'slug':{'write_only': True},
        }

 
        

    def update(self, instance, validated_data):
        print(validated_data) 
        username = self.validated_data['username'] or None
        email = self.validated_data['email'] or None
        first_name = self.validated_data['profile']['first_name']  or None
        last_name = self.validated_data['profile']['last_name'] or None
        address = self.validated_data['profile']['address'] or None
        phone_number = self.validated_data['profile']['phone_number'] or None


        profile = Profile.objects.get(user=instance)

            

        if username != '' and username != None :
            instance.username = username
        check_mail = User.objects.filter(email=email).exclude(id=instance.id).count()
        if check_mail > 0 :
            raise ValueError(
                'Email already exist.'
            )
        else:
            instance.email = email


        profile.first_name = first_name
        profile.last_name = last_name
        profile.address = address 
        profile.phone_number = phone_number
        instance.profile.first_name = first_name
        instance.profile.last_name = last_name
        instance.profile.address = address 
        instance.profile.phone_number = phone_number


        try :
            image = self.validated_data['profile']['profile_image']
            profile.profile_image = image 
            profile.save()
            instance.profile.profile_image = image
        except :
            profile.save()

        
        instance.save()

        

        return instance

  

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password' ]

        extra_kwargs = {
            'password':{'write_only': True},
        }
 

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        user = User(username=username , email=email)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : 'Email already exist'})

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': 'Username already exist'})

        if len(password) < 8:
            raise serializers.ValidationError({'error': 'password must be at least eight characters'})

        user.set_password(password)
        user.save()
        return user





class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields =  ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=1,max_length=30, write_only=True)
    token = serializers.CharField(min_length=1,max_length=300, write_only=True)
    uuidb64 = serializers.CharField(min_length=1,max_length=100, write_only=True)

    class Meta:
        fields = ['password']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uuidb64 = attrs.get('uuidb64')
            id = force_str(urlsafe_base64_decode(uuidb64))
            user = User.objects.get(id=id)
            if PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(password)
                user.save()
            else:
                raise AuthenticationError('The reset link is invalid', 401)
        except Exception as e :
            raise AuthenticationError('The reset link is invalid', 401)
        return super().validate(attrs)










class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


    def save(self):
        request = self.context.get('request')
        old_password = self.validated_data['old_password']
        new_password = self.validated_data['new_password']
        user = User.objects.get(id=request.user.id)
        if not user.check_password(old_password):
            raise serializers.ValidationError({'error': 'Incorrect password','status': status.HTTP_400_BAD_REQUEST})
        user.set_password(new_password)
        user.save()
        return user
        
        

