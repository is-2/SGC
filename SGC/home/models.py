from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user        = models.OneToOneField(User)
    telephone   = models.CharField(max_length=100)
    observation = models.CharField(max_length=100)
    address     = models.CharField(max_length=100)
    
    class Meta:
        permissions = (("puede_crear_usuario","Puede crear usuario"),
                       ("puede_modificar_usuario","Puede modificar usuario"),
                       ("puede_eliminar_usuario", "Puede eliminar usuario"),
                       ("puede_crear_rol","Puede crear rol"),
                       ("puede_modificar_rol", "Puede modificar rol"),
                       ("puede_eliminar_rol","Puede eliminar rol"),)


    