# -*- coding: utf-8 -*-
from django.db import models
from adm.models import Phase
import reversion
# Create your models here.
class AttributeType(models.Model):
    """
    Tipo de Atributo es una clase esqueleto que formará parte de un Tipo de Ítem. Esta clase indicará
    de qué tipo de Atributo debe ser el Atributo del Ítem a la hora de instanciar un Tipo de Ítem.
    """
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=100)
    attr_type = models.CharField("Type", max_length=20)
    
    class Meta:
        permissions = (("puede_crear_tipo_de_atributo",u"Puede crear Tipo de Atributo"),
                       ("puede_modificar_tipo_de_atributo",u"Puede modificar Tipo de Atributo"),
                       ("puede_eliminar_tipo_de_atributo",u"Puede eliminar Tipo de Atributo"),)
        
    def __unicode__(self):
        return self.name

class Attribute(models.Model):
    """
    Atributo es la instancia del Tipo de Atributo. Esta clase forma parte de un Ítem y podrá asignarle
    un valor dependiendo del Tipo de Atributo que sea. Puede ser Numérico, Cadena, Booleano o Fecha.
    """
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=100)
    type = models.CharField("Type", max_length=20)
    attr_int = models.IntegerField("Integer", null=True)
    attr_str = models.CharField("String", max_length=100, null=True, blank=True)
    attr_bool = models.BooleanField("Boolean", default=False)
    attr_date = models.DateField("Date", null=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    
    class Meta:
        permissions = (("puede_crear_atributo",u"Puede crear Atributo"),
                       ("puede_modificar_atributo",u"Puede modificar Atributo"),
                       ("puede_eliminar_atributo",u"Puede eliminar Atributo"),)
        
    def __unicode__(self):
        return self.name
    
class ItemType(models.Model):
    """
    Tipo de Ítem es una clase esqueleto que luego será instanciada por Ítem. Esta clase indicará
    de qué Tipo de Ítem deber ser el Ítem.
    """
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=100)
    
    # Associated Attribute Types.
    attribute_types = models.ManyToManyField("AttributeType")
    
    class Meta:
        permissions = (("puede_crear_tipo_de_item",u"Puede crear Tipo de Ítem"),
                       ("puede_modificar_tipo_de_item",u"Puede modificar Tipo de Ítem"),
                       ("puede_eliminar_tipo_de_item",u"Puede eliminar Tipo de Ítem"),)
        
    def __unicode__(self):
        return self.name

class Item(models.Model):
    """
    Ítem es la clase que instancia a Tipo de Ítem. Es la clase que será utilizada como base para
    ser asignados a las fases.
    """
    name        = models.CharField('Name', max_length=100, unique=True)
    description = models.CharField('Description', max_length=100)
    cost        = models.IntegerField('Cost')
    
    ACTIVE      = 0
    FINISHED    = 1
    DELETED     = 2
    
    STATUS_CHOICES = ((ACTIVE, 'Activo'),
                      (FINISHED, 'Finalizado'),
                      (DELETED, 'Eliminado'),)
    
    status      = models.SmallIntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    predecessor = models.ForeignKey('Item', blank=True, null=True, on_delete=models.SET_NULL)
    baseline    = models.ForeignKey('BaseLine', blank=True, null=True, on_delete=models.SET_NULL)
    phase       = models.ForeignKey('adm.Phase', blank=True, null=False, on_delete=models.CASCADE)
    
    class Meta:
        permissions = (("puede_crear_item", u"Puede crear Ítem"),
                       ("puede_modificar_item", u"Puede modificar Ítem"),
                       ("puede_eliminar_item", u"Puede eliminar Ítem"),)
        
    def __unicode__(self):
        return self.name
    
reversion.register(Item, follow=["attribute_set"])
reversion.register(Attribute)

BASELINE_STATES = (
    (0, "Abierto"),
    (1, "Cerrado"),
)

class BaseLine(models.Model):
    """
    """
    name = models.CharField(max_length=30, blank=False)
    state = models.IntegerField(choices= BASELINE_STATES, default=0)
    phase = models.ForeignKey(Phase)
