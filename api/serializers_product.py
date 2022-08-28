from rest_framework import serializers
from .models import *
from rest_framework import serializers
from account.models import User , Profile 
from product.models import Company , ProductCategory , ProductImage, Product


 




class CompanyProductSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    selling_price = serializers.IntegerField(read_only=True)
    description = serializers.CharField(read_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    total_dislikes = serializers.IntegerField(read_only=True)



    # fields = ['slug','selling_price', 'image', 'description', 'category' , 'company', 'total_likes','total_dislikes'  ]


# Custom serializer to display company name
class CustomCompanySerializer(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'name':value.name
        }



class CompanyDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Company
        fields = ['pk','slug','name', 'address' , 'email', 'phone_number', 'active','products']

        extra_kwargs = {
            'slug':{'read_only': True},
            'active':{'read_only': True},
        }

    
    def get_products(self, obj ):
        company_product = Product.objects.filter(company__id=obj.id)
        return CompanyProductSerializer(company_product , many=True).data  




# All companies serializer class 
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__' 
        # fields = ['slug','name', 'address' , 'email', 'phone_number', 'active', ]


# Custom serializer to display category name
class CustomCategorySerializer(serializers.RelatedField):
    
    def to_representation(self, value):
        return {
            'name':value.name
        }





class ProductSerializer(serializers.ModelSerializer):
    # category = CustomCategorySerializer(many=True, read_only=True)
    # company = serializers.PrimaryKeyRelatedField(read_only=True)
    # company = serializers.SerializerMethodField(read_only=True)
    # company = serializers.PrimaryKeyRelatedField(source='company.name', read_only=True)
    class Meta: 
        model = Product
        # fields = '__all__' 
        fields = ['pk','slug','name', 'price',  'description', 'category' , 'company', 'total_likes','total_dislikes'  ]

        extra_kwargs = {
            'slug':{'read_only': True},
            'active':{'read_only': True},
        }


    # def get_company(self, obj):
    #     return obj.company.name






class ProductWithDiscountSerializer(serializers.ModelSerializer):
    category = CustomCategorySerializer(many=True, read_only=True)
    company = serializers.SerializerMethodField(read_only=True)
    class Meta: 
        model = Product
        fields = ['slug','name', 'price','selling_price', 'image', 'description', 'category' , 'company', 'total_likes','total_dislikes'  ]


    def get_company(self, obj):
        return obj.company.name

    
