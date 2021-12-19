from django.contrib import admin

from favorites.models import Favorite, Like

admin.site.register(Like)
admin.site.register(Favorite)
