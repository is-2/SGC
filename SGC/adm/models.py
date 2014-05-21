from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PROYECT_STATES = (
    (0, "Pendiente"),
    (1, "Activo"),
    (2, "Finalizado"),
)

class Project(models.Model):
    name = models.CharField("project's name", max_length=100)
    description = models.CharField("description", max_length=100)   
    state = models.IntegerField(max_length=30,choices= PROYECT_STATES, default=0)
    users = models.ManyToManyField(User, related_name = "projects")
    committee = models.ManyToManyField(User, related_name = "committee")
        
    class Meta:
        permissions = (("puede_crear_proyecto","Puede crear proyecto"),
                       ("puede_modificar_proyecto","Puede modificar proyecto"),
                       ("puede_eliminar_proyecto","Puede eliminar proyecto"),)

PHASE_STATES = (
    (0, "Inicial"),
    (1, "Desarrollo"),
    (2, "Finalizado"),
)

class Phase(models.Model):
    """
    
    """
    name = models.CharField(max_length=30, blank=False)
    state = models.IntegerField(max_length=30,choices=PHASE_STATES, default=0)
    order = models.IntegerField(max_length=30, blank=False)
    project = models.ForeignKey(Project)