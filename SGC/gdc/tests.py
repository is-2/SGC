from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from gdc.models import ModificationRequest
import views
# Create your tests here.
class ModificationRequestTests(TestCase):
    """
    """
    
    fixtures = ['gdc.json']
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='alfredo', email='akirashimosoeda@gmail.com', password='wtf')
        
    def tearDown(self):
        del self.factory
        del self.user
        
    def test_list_requests(self):
        request = self.factory.get(reverse('list_requests'))
        request.user = self.user
        response = views.list_requests(request)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_create_request_get(self):
        ctx = {'id_item':1}
        request = self.factory.get(reverse('create_request', kwargs=ctx))
        request.user = self.user
        response = views.create_request(request,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_create_request_post(self):
        ctx = {'id_item':1}
        request = self.factory.post(reverse('create_request', kwargs=ctx), {'name':'test2', 'description':'test2'})
        request.user = self.user
        response = views.create_request(request,1)
        #self.assertEqual(response.status_code, 302)
        
    def test_accept_request_get(self):
        ctx={'id_request':1}
        request = self.factory.get(reverse('accept_request', kwargs=ctx))
        request.user = self.user
        response = views.accept_request(request,1)
        self.assertEqual(response.status_code, 302, "No ha retornado la pagina")
        
    def test_reject_request_get(self):
        ctx={'id_request':1}
        request = self.factory.get(reverse('reject_request', kwargs=ctx))
        request.user = self.user
        response = views.reject_request(request,1)
        self.assertEqual(response.status_code, 302, "No ha retornado la pagina")
        
    def test_visualize_request_get(self):
        ctx={'id_request':1}
        request = self.factory.get(reverse('visualize_request', kwargs=ctx))
        request.user = self.user
        response = views.visualize_request(request,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_list_pending(self):
        request = self.factory.get(reverse('list_pending'))
        request.user = self.user
        response = views.list_pending(request)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_modify_pending_item_get(self):
        ctx={'id_item':1}
        request = self.factory.get(reverse('modify_pending_item', kwargs=ctx))
        request.user = self.user
        response = views.modify_pending_item(request,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_modify_pending_item_post(self):
        ctx = {'id_item':1}
        request = self.factory.post(reverse('modify_pending_item', kwargs=ctx), {'name':'test2', 'description':'test2'})
        request.user = self.user
        response = views.create_request(request,1)
        #self.assertEqual(response.status_code, 302, "No ha retornado la pagina")
        
    def test_list_pending_attr_get(self):
        ctx={'id_item':1}
        request = self.factory.get(reverse('list_pending_attr', kwargs=ctx))
        request.user = self.user
        response = views.list_pending_attr(request,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_set_pending_attr_value_get(self):
        ctx={'id_attr':1}
        request = self.factory.get(reverse('set_pending_attr_value', kwargs=ctx))
        request.user = self.user
        response = views.set_pending_attr_value(request,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_set_pending_attr_value_post(self):
        ctx={'id_attr':1}
        request = self.factory.post(reverse('set_pending_attr_value', kwargs=ctx), {'attr_int':1})
        request.user = self.user
        response = views.set_pending_attr_value(request,1)
        self.assertEqual(response.status_code, 302, "No ha retornado la pagina")
        
    def test_list_pending_predecessors_get(self):
        ctx={'id_item':1}
        request = self.factory.get(reverse('list_pending_predecessors', kwargs=ctx))
        request.user = self.user
        response = views.list_pending_predecessors(request,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def set_finish_pending_item(self):
        ctx={'id_item':1}
        request = self.factory.get(reverse('finish_pending_item', kwargs=ctx))
        request.user = self.user
        response = views.finish_pending_item(request,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")