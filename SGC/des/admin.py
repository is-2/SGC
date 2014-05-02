from django.contrib import admin
from models import AttributeType, NumericType, StringType, BooleanType, DateType
# Register your models here.
admin.site.register(AttributeType)
# Register generic attribute types models
admin.site.register(NumericType)
admin.site.register(StringType)
admin.site.register(BooleanType)
admin.site.register(DateType)