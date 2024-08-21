from django.contrib import admin

# Register your models here.

from .models import Poll, Response, Histogram
admin.site.register(Poll)
admin.site.register(Response)
admin.site.register(Histogram)