from django.contrib import admin
from models import ItemType, AttributeType, Attribute, Item
import reversion

# Register your models here.
admin.site.register(ItemType)
admin.site.register(AttributeType)
admin.site.register(Attribute)

class ItemAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Item, ItemAdmin)