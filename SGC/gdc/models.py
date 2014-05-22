from django.db import models
from django.contrib.auth.models import User
# Custom imports
from des.models import Item
# Create your models here.
class ModificationRequest(models.Model):
    """
    Peticion de cambio es una clase que gestiona una peticion de modificacion de un item.
    Los items que estan finalizados solo pueden ser modificados con el uso de la peticion.
    La peticion envia mensaje a los comites de cambios para aceptar o rechazar el pedido
    de cambio.
    """
    committee = models.ManyToManyField(User)
    item = models.ForeignKey(Item)
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description', max_length=300)
    total_requests = models.IntegerField('Total Requests')
    accepted_requests = models.IntegerField('Accepted Requests', default=0)
    rejected_requests = models.IntegerField('Rejected Requests', default=0)
    
    class Meta:
        permissions = (("puede_crear_peticion_de_cambio",u"Puede crear Peticion de cambio"),
                       ("puede_modificar_peticion_de_cambio",u"Puede modificar Peticion de cambio"),
                       ("puede_eliminar_peticion_de_cambio",u"Puede eliminar Peticion de cambio"),)
        
    def __unicode__(self):
        return self.title