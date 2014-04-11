from django.db import models

class cliente(models.Model):
    nombre      = models.CharField(max_length=200)
    apellido    = models.CharField(max_length=200)
    status      = models.BooleanField(default=True)
    def __unicode__(self):
        nombreCompleto = "%s %s"%(self.nombre,self.apellido)
        return nombreCompleto
    
class producto(models.Model):
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=300)
    status      = models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre

# REAL MODELS

class user(models.Model):
    name        = models.CharField(max_length=200)
    lastname    = models.CharField(max_length=200)
    status      = models.BooleanField(default=True)
    email       = models.CharField(max_length=200)
    phonenum    = models.CharField(max_length=200)
    direction   = models.CharField(max_length=200)
    observation = models.CharField(max_length=200)
    def __unicode__(self):
        fullname = "%s %s"%(self.name,self.lastname)
        return fullname