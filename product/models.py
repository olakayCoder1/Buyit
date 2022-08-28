from django.db import models
from django.db.models import Q
from account.models import User
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
import secrets
import string
# Create your models here.
from django.db.models import QuerySet , Manager



class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    slug = models.CharField(max_length=100, null=True, blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", limit_choices_to={'is_staff': True})
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)


    def __str__(self):
        return self.name


@receiver(post_save , sender=Company)
def company_signal(sender,created, instance , **kwarg):
    if created :
        alphabet = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(alphabet) for i in range(20))
        user_identifier = random_string+str(instance.id)
        instance.slug = user_identifier
        instance.save()






class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
# Custom queryset for searching product the search uses the following
# product name
# product description
# Product category name ( a many to many relation to the product table )
class ProductQuerySet(models.QuerySet):

    def search(self, query ):
        q = Q(name__icontains=query) | Q(description__icontains=query) |  Q(category__name__icontains=query)
        return self.filter(q)

# Custom model Manager for searching product the search uses the following
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model , using=self._db)

    def search(self , query):
        return self.get_queryset().search(query)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=100,unique=True, blank=True, null=True)
    discount_rate = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(ProductCategory, related_name="category")
    company = models.ForeignKey(Company, on_delete=models.CASCADE , related_name="company")
    likes = models.ManyToManyField(User,  blank=True , related_name="liked_by")
    dislikes = models.ManyToManyField(User,  blank=True , related_name="disliked_by")

    def __str__(self):
        return f'{self.name} , {self.price}'


    objects =  ProductManager()

    @property
    def selling_price(self):
        normal_price = self.price
        discount_percentage = self.discount_rate
        if self.discount_rate == 0 :
            return self.price
        return self.price - ((normal_price * discount_percentage ) / 100 )
    

    @property
    def total_likes(self):
        #get the count of users that like this product
        likes = self.likes.all().count()
        return likes

    @property
    def total_dislikes(self):
        #get the count of users that dislike this product
        dislikes = self.dislikes.all().count()
        return dislikes

    
       


@receiver(post_save , sender=Product)
def product_signal(sender,created, instance , **kwarg):
    if created :
        alphabet = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(alphabet) for i in range(20))
        user_identifier = random_string+str(instance.id)
        instance.slug = user_identifier
        instance.save()





def upload_to(instance, filename):
    return 'products/images/{filename}'.format(filename=filename)

class ProductImage(models.Model):
    product = models.ManyToManyField(Product)
    image  = models.ImageField(upload_to=upload_to)


# class PasswordResetToken




from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.core.mail import send_mail

@receiver(reset_password_token_created)
def password_reset_token_created(sender ,instance ,reset_password_token , *args , **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        "Password Reset for {title}".format(title="My website"),
        email_plaintext_message,
        "olakay@gmail.com",
        [reset_password_token.user.email]
    )