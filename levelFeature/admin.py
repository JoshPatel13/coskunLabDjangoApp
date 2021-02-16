from django.contrib import admin
from .models import LevelReading, Livestream

# Register your models here.
admin.site.register(LevelReading)
admin.site.register(Livestream)
