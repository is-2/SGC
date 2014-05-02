from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
# Create your models here.
class AttributeType(models.Model):
    name = models.CharField("Attribute's name", max_length=100)
    description = models.CharField("Description", max_length=100)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        permissions = (("puede_crear_tipo_de_atributo","Puede crear tipo de atributo"),
                       ("puede_modificar_tipo_de_atributo","Puede modificar tipo de atributo"),
                       ("puede_eliminar_tipo_de_atributo","Puede eliminar tipo de atributo"),)
        
    def __unicode__(self):
        return self.name
    
# Generic classes for AttributeType
class NumericType(models.Model):
    value = models.IntegerField()
    
class StringType(models.Model):
    value = models.CharField(max_length=100)
    
class BooleanType(models.Model):
    value = models.BooleanField()
    
class DateType(models.Model):
    value = models.DateField()