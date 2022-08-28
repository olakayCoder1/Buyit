from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Profile
# Register your models here.


class UserAdmin(UserAdmin):
    ordering= ('-date_joined',)
    list_filter = ['username','email']
    list_display = ['username','email','is_active','is_staff']
    search_fields =  ('username','email')
    fieldsets = (
        (None, { 'fields': ('username','email')}),
        ('Permissions',{'fields':('is_staff','is_active','is_superuser','groups',"user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),}),)
        
    

admin.site.register(User,UserAdmin)  
admin.site.register(Profile)  