from django.contrib import admin
from .models import User, FriendRequest

admin.site.register([User, FriendRequest])
