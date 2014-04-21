from django.db import models
from django.contrib.auth.models import User

# PERMISSION
class Permission(models.Model):
    """
    Clase que especifica el permiso mediante un codigo.
    """
    name     = models.CharField(max_length=30, blank=False)
    
    def __unicode__(self):
        return self.name

# ROLE
class Role(models.Model):
    """
    Clase que especifica el rol. Entre sus atributos se encuentran los permisos.
    """
    name        = models.CharField(max_length=30, blank=False)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=False)
    
    def __unicode__(self):
        return self.name

# PROJECT
class Project(models.Model):
    """
    
    """
    name = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=100, blank=False)
    roles = models.ManyToManyField(Role, null=True, blank=True)
    committee = models.ManyToManyField(User, null=True, blank=True)
    #phases = models.ManyToManyField(Phase, null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
# USER
User.add_to_class('firstName', models.CharField(max_length=100, blank=True))
User.add_to_class('lastName', models.CharField(max_length=100, blank=True))
User.add_to_class('status', models.BooleanField(default=True))
User.add_to_class('phonenum', models.CharField(max_length=100, blank=True))
User.add_to_class('address', models.CharField(max_length=100, blank=True))
User.add_to_class('observation', models.CharField(max_length=100, blank=True))
User.add_to_class('roles', models.ManyToManyField(Role, null=True, blank=True))