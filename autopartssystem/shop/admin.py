from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Brand)
admin.site.register(models.Car)
admin.site.register(models.Type)
admin.site.register(models.Car_Type)
admin.site.register(models.Part)
admin.site.register(models.Car_Parts)
admin.site.register(models.History)