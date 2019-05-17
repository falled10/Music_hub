from django.contrib import admin

from .models import Lessons, Likes

admin.site.register(Lessons, Likes)
