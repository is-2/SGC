from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from home.models import Client

# Define an inline admin descriptor for Client model
# which acts a bit like a singleton
class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'client'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ClientInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#Register models