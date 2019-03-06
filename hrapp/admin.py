from django.contrib import admin
from .models import Link,Vote,UserProfile,Comment
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

admin.site.register(Link)
admin.site.register(Vote)

# creating user profile within user in admin panel
#class UserProfileInline(admin.StackedInline):
 #  model = UserProfile
  # can_delete = False

class UserProfileAdmin(admin.ModelAdmin):
   list_display = ('user','bio',)

admin.site.register(UserProfile,UserProfileAdmin)

admin.site.register(Comment)

