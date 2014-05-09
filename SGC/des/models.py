from django.db import models
# Create your models here.
class ItemType(models.Model):
    name = models.CharField("Attribute's name", max_length=100)
    description = models.CharField("Description", max_length=100)
    attributes = models.ManyToManyField("Attribute")
    class Meta:
        permissions = (("puede_crear_tipo_de_item","Puede crear tipo de item"),
                       ("puede_modificar_tipo_de_item","Puede modificar tipo de item"),
                       ("puede_eliminar_tipo_de_item","Puede eliminar tipo de item"),)
        
    def __unicode__(self):
        return self.name
    
class AttributeType(models.Model):
    name = models.CharField("Attribute's name", max_length=100)
    description = models.CharField("Description", max_length=100)
    choice = models.IntegerField("Choice")
    
    class Meta:
        permissions = (("puede_crear_tipo_de_atributo","Puede crear tipo de atributo"),
                       ("puede_modificar_tipo_de_atributo","Puede modificar tipo de atributo"),
                       ("puede_eliminar_tipo_de_atributo","Puede eliminar tipo de atributo"),)
        
    def __unicode__(self):
        return self.name
    
class Attribute(models.Model):
    type = models.ForeignKey('AttributeType', null=True)
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=100)
    attr_int = models.IntegerField("Integer", null=True)
    attr_str = models.CharField("String", max_length=100, null=True, blank=True)
    attr_bool = models.BooleanField("Boolean", default=False)
    attr_date = models.DateField("Date", null=True)
    
    class Meta:
        permissions = (("puede_crear_atributo","Puede crear atributo"),
                       ("puede_modificar_atributo","Puede modificar atributo"),
                       ("puede_eliminar_atributo","Puede eliminar atributo"),)
        
    def __unicode__(self):
        return self.name

class Item(models.Model):
    name = models.CharField('Name', max_length=100)
    description = models.CharField('Description', max_length=100)
    type = models.ForeignKey('ItemType', null=True)
    
    class Meta:
        permissions = (("puede_crear_item", "Puede crear item"),
                       ("puede_modificar_item", "Puede modificar item"),
                       ("puede_eliminar_item", "Puede eliminar item"),)
        
    def __unicode__(self):
        return self.name