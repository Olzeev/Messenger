from django.contrib import admin
from .models import *

class UserAvatar(admin.ModelAdmin):
    list_display = ["user_info_id", "avatar"]


# Register your models here.
admin.site.register(User_blocked)
admin.site.register(Message)
admin.site.register(User_info, UserAvatar)
admin.site.register(Group)
admin.site.register(Group_ref)

