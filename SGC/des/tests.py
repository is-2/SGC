from django.test import TestCase
from django.utils import unittest
from django.test.client import Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Custom imports
from des.models import AttributeType, ItemType
import views
# Create your tests here.
class AttributeTypeTests(TestCase):
    """
    """
    # Set a fixture to fill test database.
    fixtures = ['des.json']
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='akira', email='akirashimosoeda@gmail.com', password='wtf')
        
    def tearDown(self):
        del self.factory
        del self.user
        
    def test_list_attribute_types(self):
        request = self.factory.get(reverse('list_attribute_types'))
        request.user = self.user
        response = views.list_attribute_types(request)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_create_attribute_type_get(self):
        request = self.factory.get(reverse('create_attribute_type'))
        request.user = self.user
        response = views.create_attribute_type(request)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_create_attribute_type_post(self):
        request = self.factory.post(reverse('create_attribute_type'), {'name':'test' , 'description':'test'})
        request.user = self.user
        response = views.create_attribute_type(request)
        self.assertEqual(response.status_code, 200, "No debe contener campos obligatorios vacios")
        
    def test_modify_attribute_type_get(self):
        AttributeType.objects.create(name='test', description='test')
        pk = AttributeType.objects.get(name='test').pk
        # Create an instance of a GET request.
        ctx={'id_attribute_type':1}
        request = self.factory.get(reverse('modify_attribute_type', kwargs=ctx))
        request.user = self.user
        response = views.modify_attribute_type(request, 1)###
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    def test_modify_attribute_type_post(self):
        AttributeType.objects.create(name='test', description='test')
        ctx={'id_attribute_type':1}
        request = self.factory.post(reverse('modify_attribute_type', kwargs=ctx), {'name':'test2', 'description':'test2', 'attr_type':'1'})
        request.user = self.user
        response = views.modify_attribute_type(request, 1)
        self.assertEqual(response.status_code, 302, "No debe contener campos obligatorios vacios")
        
    def test_delete_attribute_type_get(self):
        AttributeType.objects.create(name='test', description='test')
        ctx={'id_attribute_type':1}
        request = self.factory.get(reverse('delete_attribute_type', kwargs=ctx))
        request.user = self.user
        response = views.delete_attribute_type(request, 1)
        self.assertEqual(response.status_code, 200)
        
    def test_delete_attribute_type_post(self):
        AttributeType.objects.create(name='test', description='test')
        ctx={'id_attribute_type':1}
        request = self.factory.post(reverse('delete_attribute_type', kwargs=ctx))
        request.user = self.user
        response = views.delete_attribute_type(request, 1)
        self.assertEqual(response.status_code, 302)
        
    def test_visualize_attribute_type_get(self):
        id = 1
        ctx={'id_attribute_type':id}
        request = self.factory.get(reverse('visualize_attribute_type', kwargs=ctx))
        request.user = self.user
        response = views.visualize_attribute_type(request, id)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
class ItemTypeTests(TestCase):
    """
    """
    fixtures = ['des.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='akira', email='akirashimosoeda@gmail.com', password='wtf')
        
    def tearDown(self):
        del self.factory
        del self.user
        
    def test_list_item_types(self):
        request = self.factory.get(reverse('list_item_types'))
        request.user = self.user
        response = views.list_attribute_types(request)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
            
    def test_create_item_type_get(self):
        request = self.factory.get(reverse('create_item_type'))
        request.user = self.user
        response = views.create_item_type(request)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_create_item_type_post(self):
        request = self.factory.post(reverse('create_item_type'), {'name':'test' , 'description':'test'})
        request.user = self.user
        response = views.create_item_type(request)
        self.assertEqual(response.status_code, 302)
        
    def test_modify_item_type_get(self):
        ctx = {'id_item_type':1}
        request = self.factory.get(reverse('modify_item_type', kwargs=ctx))
        request.user = self.user
        response = views.modify_item_type(request, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    def test_modify_item_type_post(self):
        ctx = {'id_item_type':1}
        request = self.factory.post(reverse('modify_item_type', kwargs=ctx), {'name':'test' , 'description':'test'})
        request.user = self.user
        response = views.modify_item_type(request, 1)
        self.assertEqual(response.status_code, 302)
        
    def test_delete_item_type_get(self):
        ctx = {'id_item_type':1}
        request = self.factory.get(reverse('delete_item_type', kwargs=ctx))
        request.user = self.user
        response = views.delete_item_type(request, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_delete_item_type_post(self):
        ctx = {'id_item_type':1}
        request = self.factory.post(reverse('delete_item_type', kwargs=ctx), {'name':'test' , 'description':'test'})
        request.user = self.user
        response = views.delete_item_type(request, 1)
        self.assertEqual(response.status_code, 302)
        
    def test_visualize_item_type(self):
        ctx = {'id_item_type':2}
        request = self.factory.get(reverse('visualize_item_type', kwargs=ctx))
        request.user = self.user
        response = views.visualize_item_type(request, 2)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_assign_attribute_type(self):
        ctx = {'id_item_type':2}
        request = self.factory.get(reverse('assign_attribute_type', kwargs=ctx))
        request.user = self.user
        response = views.assign_attribute_type(request, 2)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_grant_attribute_type(self):
        ctx = {'id_item_type':2, 'id_attr_type':1}
        request = self.factory.get(reverse('grant_attribute_type', kwargs=ctx))
        request.user = self.user
        response = views.grant_attribute_type(request, 1, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_deny_attribute_type(self):
        ctx = {'id_item_type':2, 'id_attr_type':1}
        request = self.factory.get(reverse('deny_attribute_type', kwargs=ctx))
        request.user = self.user
        response = views.deny_attribute_type(request, 2, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
                
class ItemTests(TestCase):
    """
    """
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='akira', email='akirashimosoeda@gmail.com', password='wtf')
        
    def tearDown(self):
        del self.factory
        del self.user
        
    
    