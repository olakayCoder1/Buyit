from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin ,BaseUserManager
# Create your models here.
import secrets
import string

class UserManager(BaseUserManager):

    def create_user(self, username,email,password,**extra_fields):
        if not username:
            raise ValueError('Invalid username')
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(username=username , email=email , **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self,username,email,password, **extra_fields):

        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must be given is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be given is_superuser=True')
        return self.create_user(username,email,password,**extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True )
    slug = models.CharField(max_length=100, null=True , blank=True )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    


    objects= UserManager()

    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = ['username']



    def __str__(self):
        return self.username






def upload_to(instance, filename):
    return 'profiles/{filename}'.format(filename=filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100 , blank=True , null=True)
    last_name = models.CharField(max_length=100 , blank=True , null=True)
    address = models.TextField(null=True , blank=True)
    phone_number = models.CharField(max_length=20 , null=True , blank=True)
    profile_image = models.ImageField(default='profiles/image-default.png', upload_to=upload_to)


@receiver(post_save , sender=User)
def user_profile_signal(sender, instance , created , **kwarg):
    if created:
        Profile.objects.create(user = instance )
        alphabet = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(alphabet) for i in range(20))
        user_identifier = random_string+str(instance.id)
        instance.slug = user_identifier
        instance.save()