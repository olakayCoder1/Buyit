from django.shortcuts import render
from account.models import User
from product.models import ( 
    Company, 
    Product , 
    ProductCategory 
    )

from .serializers_product import (
    ProductSerializer ,
    ProductWithDiscountSerializer,
    CompanyDetailSerializer,
    CompanySerializer,
)
from .serializers import (  
    UserSerializer, 
    RegisterSerializer , 
    ResetPasswordRequestSerializer,
    SetNewPasswordSerializer,
    ChangePasswordSerializer
    
    )

from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework import generics  , mixins
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.
from .utils import get_profile_with_discount



class ChangePasswordApiView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer 
    permission_classes = [IsAuthenticated] 
    #  = User
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get_object(self):
        user = User.objects.get( id= self.request.user.id )
        print("****"*20)
        return user   

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial , context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

    # def update(self , request , *args , **kwargs ):
    #     self.object  = self.get_object
    #     print(self.object)
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         print(self.object)
    #         if not self.object.check_password(serializer.data.get("old_password")):
    #             return Response({"old_password" : ["old password is not correct"]}, status=status.HTTP_400_BAD_REQUEST)
    #         self.object.set_password(serializer.data.get('new_password'))
    #         self.object.save()
    #         response = {
    #             'status' : 'success',
    #             'code' : status.HTTP_200_OK,
    #             'message': 'Password updated successfully'
    #         }
    #         return Response(response)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        token['staff'] = user.is_staff
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str , force_str , smart_bytes ,force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



  
class PasswordResetApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        email = request.data['email']
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(force_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)

                m = f"http://{get_current_site(request)}/api/v1/password-reset/{uidb64}/{token}/"
                print(f"http://{get_current_site(request)}/api/v1/password-reset/{uidb64}/{token}/")
                return Response({'success':True , 'message': m }, status=status.HTTP_200_OK)
            except:
                # pass
                return Response({'message': 'Email sent '}, status=status.HTTP_200_OK)
    

class PasswordTokenCheckApi(generics.GenericAPIView):
    def get(self, request, uuidb64 , token):
        try:
            id = smart_str(urlsafe_base64_decode(uuidb64))
            user = User.objects.get(id=id)
            print(PasswordResetTokenGenerator().check_token(user, token))
            if PasswordResetTokenGenerator().check_token(user, token):
                return Response({'success':True , 'message':'Token is valid', 'uuidb64': uuidb64, 'token': token }, status=status.HTTP_200_OK)

            return Response({'error':'Token is not valid, try again'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except DjangoUnicodeDecodeError as identifier:
            # print(PasswordResetTokenGenerator().check_token(user, token))
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self , request,  uuidb64 , token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password updated successfully'}, status=status.HTTP_200_OK)






class UserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):  
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'


    # def perform_update(self, serializer):
    #     # print(serializer.validated_data)
    #     # username = serializer.validated_data['username']
    #     # email = serializer.validated_data['email']
    #     # # profile = serializer.validated_data['profile']
    #     # print(username)
    #     # print(profile['first_name'])
    #     # print("********"*20)
    #     # instance = serializer.save()
    #     return super().perform_update(serializer)



class UserCreateApiView(generics.CreateAPIView):  
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        return super().perform_create(serializer)


class ProductListCreateAPIView(generics.ListCreateAPIView):  
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class ProductSearchAPIView(generics.ListAPIView):  
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args , **kwargs):
        qs = super().get_queryset( *args , **kwargs)
        q = self.request.GET.get("q")
        if q == None :
            return None
        result = qs.search(q)

        return result


class ProductWithDiscountListApiView(generics.ListAPIView):  
    queryset = Product.objects.all()
    serializer_class = ProductWithDiscountSerializer 

    def get_queryset(self):
        return get_profile_with_discount()


class ProductCreateApiView(generics.CreateAPIView):  
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    # lookup_field = 'pk'

class ProductDetailApiView(generics.RetrieveAPIView):  
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    # lookup_field = 'pk'





class CompanyListCreateApiView(generics.ListCreateAPIView):  
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class CompanyDetailApiView(generics.RetrieveUpdateAPIView):  
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'pk'


class CompanyUpdateDeleteApiView(generics.RetrieveUpdateAPIView):  
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'pk'

    



# product liking view 
@api_view(['GET'])
def like_product_view(request, pk):
    user = User.objects.get(id=request.user.id)
    product = get_object_or_404(Product , pk=pk)
    # add the authenticated user to the users that like the product
    has_disliked = product.likes.filter(id=user.id)
    if has_disliked != None :
        product.dislikes.remove(user)
    return Response(status=status.HTTP_200_OK)

 
@api_view(['GET'])
def dislike_product_view(request, pk):
    user = User.objects.get(id=request.user.id)
    product = get_object_or_404(Product , pk=pk)
    has_liked = product.likes.filter(id=user.id)

    if has_liked != None :
        product.likes.remove(user)
    product.dislikes.add(user)  
    # add the authenticated user to the users that like the product
    # product.dislikes.add(user)
    return Response(status=status.HTTP_200_OK)
