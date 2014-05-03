from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField("project's name", max_length=100)
    description = models.CharField("description", max_length=100)
    
    #leader = models.ForeignKey(User, "the related leader")
    #committees = models.ManyToManyField(User, through='ProjectMembership')
    #groups = models.ManyToManyField(Group, "list of groups")
    
    class Meta:
        permissions = (("puede_crear_proyecto","Puede crear proyecto"),
                       ("puede_modificar_proyecto","Puede modificar proyecto"),
                       ("puede_eliminar_proyecto","Puede eliminar proyecto"),)
        