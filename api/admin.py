from django.contrib import admin
from.models import Hobby, CustomUser, UserHobby, FriendRequest


admin.site.register(Hobby)
admin.site.register(CustomUser)
admin.site.register(UserHobby)
admin.site.register(FriendRequest) 