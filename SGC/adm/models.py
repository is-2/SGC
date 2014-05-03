from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField("project's name", max_length=100)
    description = models.CharField("description", max_length=100)
    users = models.ManyToManyField(User, related_name = "users")
    committee = models.ManyToManyField(User, related_name = "committee")
    
    class Meta:
        permissions = (("puede_crear_proyecto","Puede crear proyecto"),
                       ("puede_modificar_proyecto","Puede modificar proyecto"),
                       ("puede_eliminar_proyecto","Puede eliminar proyecto"),)

class Phase(models.Model):
    """
    
    """
    name = models.CharField(max_length=30, blank=False)
    project = models.ForeignKey(Project)        