from django.contrib import admin

# Register your models here.
from login.models import UserLogin, Word, Category, Game

admin.site.register(UserLogin)
admin.site.register(Word)
admin.site.register(Category)
admin.site.register(Game)
