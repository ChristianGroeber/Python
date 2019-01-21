from django.contrib import admin

# Register your models here.
from login.models import UserLogin

admin.site.register(UserLogin)