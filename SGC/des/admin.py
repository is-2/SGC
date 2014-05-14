from django.contrib import admin
from models import ItemType, AttributeType, Attribute, Item
import reversion

# Register your models here.
admin.site.register(ItemType)
admin.site.register(AttributeType)
admin.site.register(Attribute)

class AttributeInlineAdmin(admin.StackedInline):
    model = Attribute
    
class ItemAdmin(reversion.VersionAdmin):
    inlines = [AttributeInlineAdmin,]

admin.site.register(Item, ItemAdmin)