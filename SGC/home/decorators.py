from adm.models import Role, Permission
from django.http.response import HttpResponseRedirect
from functools import wraps

def permission_required(permission):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            roles = Role.objects.filter(user__id=request.user.id)
            for role in roles:
                permissios = Permission.objects.filter(role__id=role.id)
                for perm in permissios:
                    if perm.name == permission:
                        return func(request, *args, **kwargs)
            return HttpResponseRedirect('/denied_access/')
        return wraps(func)(inner_decorator)
    return decorator