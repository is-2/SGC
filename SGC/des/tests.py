from django.test import TestCase
from django.utils import unittest
from django.test.client import Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Custom imports
from des.models import AttributeType, ItemType, BaseLine
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
        ctx = {'id_attribute_type':1}
        request = self.factory.get(reverse('modify_attribute_type', kwargs=ctx))
        request.user = self.user
        response = views.modify_attribute_type(request, 1)  # ##
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    def test_modify_attribute_type_post(self):
        AttributeType.objects.create(name='test', description='test')
        ctx = {'id_attribute_type':1}
        request = self.factory.post(reverse('modify_attribute_type', kwargs=ctx), {'name':'test2', 'description':'test2', 'attr_type':'1'})
        request.user = self.user
        response = views.modify_attribute_type(request, 1)
        self.assertEqual(response.status_code, 302, "No debe contener campos obligatorios vacios")
        
    def test_delete_attribute_type_get(self):
        AttributeType.objects.create(name='test', description='test')
        ctx = {'id_attribute_type':1}
        request = self.factory.get(reverse('delete_attribute_type', kwargs=ctx))
        request.user = self.user
        response = views.delete_attribute_type(request, 1)
        self.assertEqual(response.status_code, 200)
        
    def test_delete_attribute_type_post(self):
        AttributeType.objects.create(name='test', description='test')
        ctx = {'id_attribute_type':1}
        request = self.factory.post(reverse('delete_attribute_type', kwargs=ctx))
        request.user = self.user
        response = views.delete_attribute_type(request, 1)
        self.assertEqual(response.status_code, 302)
        
    def test_visualize_attribute_type_get(self):
        id = 1
        ctx = {'id_attribute_type':id}
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
    fixtures = ['des.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='akira', email='akirashimosoeda@gmail.com', password='wtf')
        
    def tearDown(self):
        del self.factory
        del self.user
        
    def test_list_items(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.get(reverse('list_items', kwargs=ctx))
        request.user = self.user
        response = views.list_items(request,1 , 1, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    def test_create_item_get(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.get(reverse('create_item', kwargs=ctx))
        request.user = self.user
        response = views.create_item(request,1,1,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_create_item_post(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.post(reverse('create_item', kwargs=ctx), {'name':'test' , 'description':'test'})
        request.user = self.user
        response = views.create_item(request,1,1,1)
        self.assertEqual(response.status_code, 302)
        
    def test_modify_item_get(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1, 'id_item':1}
        request = self.factory.get(reverse('modify_item', kwargs=ctx))
        request.user = self.user
        response = views.modify_item(request,1,1,1,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    def test_modify_item_type_post(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1,'id_item':1}
        request = self.factory.post(reverse('modify_item', kwargs=ctx), {'name':'test' , 'description':'test'})
        request.user = self.user
        response = views.modify_item(request, 1,1,1,1)
        self.assertEqual(response.status_code, 302)
        
    def test_delete_item_get(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1,'id_item':1}
        request = self.factory.get(reverse('delete_item', kwargs=ctx))
        request.user = self.user
        response = views.delete_item(request, 1,1,1,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_delete_item_post(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1,'id_item':1}
        request = self.factory.post(reverse('delete_item', kwargs=ctx))
        request.user = self.user
        response = views.delete_item(request, 1,1,1,1)
        self.assertEqual(response.status_code, 302)
        
    def test_assign_item_type(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1,'id_item':1}
        request = self.factory.get(reverse('assign_item_type', kwargs=ctx))
        request.user = self.user
        response = views.assign_item_type(request, 1,1,1,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_add_item_type(self):
        ctx = {'id_item':1,'id_item_type':1,'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.get(reverse('add_item_type', kwargs=ctx))
        request.user = self.user
        response = views.add_item_type(request,1,1,1,1,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    def test_list_attributes(self):
        ctx = {'id_item':1,'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.get(reverse('list_attributes', kwargs=ctx))
        request.user = self.user
        response = views.list_attributes(request,1,1,1,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_set_attribute_value_get(self):
        ctx = {'id_item':1,'id_attr':1,'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.get(reverse('set_attribute_value', kwargs=ctx))
        request.user = self.user
        response = views.set_attribute_value(request,1,1,1,1,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    def test_set_attribute_value_post(self):
        ctx = {'id_item':1,'id_attr':1,'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.post(reverse('set_attribute_value', kwargs=ctx), {'attr_int':1})
        request.user = self.user
        response = views.set_attribute_value(request,1,1,1,1,1)
        self.assertEqual(response.status_code, 302)
        
    def test_item_history(self):
        ctx = {'id_item':1,'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.get(reverse('item_history', kwargs=ctx))
        request.user = self.user
        response = views.item_history(request,1,1,1,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    def test_revert_item(self):
        ctx = {'id_item':1,'id_version':1, 'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.get(reverse('revert_item', kwargs=ctx))
        request.user = self.user
        response = views.revert_item(request,1,1,1,1,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    def test_list_deleted_items(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.get(reverse('list_deleted_items', kwargs=ctx))
        request.user = self.user
        response = views.list_deleted_items(request,1,1,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_revive_item(self):
        ctx = {'id_item':1,'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.get(reverse('revive_item', kwargs=ctx))
        request.user = self.user
        response = views.revive_item(request,1,1,1,1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    
    
    
    
class BaseLineTests(TestCase):
    """
    """
    fixtures = ['des.json']
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='akira', email='akirashimosoeda@gmail.com', password='wtf')
    
    def tearDown(self):
        del self.factory
        del self.user
    
    def test_list_user_projects(self):
        
        ctx = {'id_user':1}
        request = self.factory.get(reverse('list_user_projects', kwargs=ctx))
        request.user = self.user
        response = views.list_user_projects(request, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_list_project_phases(self):
        ctx = {'id_user':1, 'id_project':1}
        request = self.factory.get(reverse('list_project_phases', kwargs=ctx))
        request.user = self.user
        response = views.list_project_phases(request, 1, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_list_phase_baseline(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.get(reverse('list_phase_baseline', kwargs=ctx))
        request.user = self.user
        response = views.list_phase_baseline(request, 1, 1, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    def test_create_baseline_get(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.get(reverse('create_baseline', kwargs=ctx))
        request.user = self.user
        response = views.create_baseline(request, 1, 1, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
    
    def test_create_baseline_post(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1}
        request = self.factory.post(reverse('create_baseline', kwargs=ctx), {'name':'bs1'})
        request.user = self.user
        response = views.create_baseline(request, 1, 1, 1)
        self.assertEqual(response.status_code, 200)
    
    def test_modify_baseline_get(self):
        
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1, 'id_baseline':1}
        
        # Create an instance of a GET request.
        request = self.factory.get(reverse('modify_baseline', kwargs=ctx))
        request.user = self.user
        response = views.modify_baseline(request, 1, 1, 1, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_modify_baseline_post(self):

        ctx = {'id_user':1, 'id_project':1, 'id_phase':1, 'id_baseline':1}
        request = self.factory.post(reverse('modify_baseline', kwargs=ctx), {'name':'test2'})
        request.user = self.user
        response = views.modify_baseline(request, 1, 1, 1, 1)
        self.assertEqual(response.status_code, 200, "No debe contener campos obligatorios vacios")
        
    def test_manage_baseline_items(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1, 'id_baseline':1}
        request = self.factory.get(reverse('manage_baseline_items', kwargs=ctx))
        request.user = self.user
        response = views.manage_baseline_items(request, 1, 1, 1, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_assign_baseline_item(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1, 'id_baseline':1, 'id_item':1}
        request = self.factory.get(reverse('assign_baseline_item', kwargs=ctx))
        request.user = self.user
        response = views.assign_baseline_item(request, 1, 1, 1, 1, 1)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")        
        
    def test_remove_baseline_item(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1, 'id_baseline':1, 'id_item':2}
        request = self.factory.get(reverse('remove_baseline_item', kwargs=ctx))
        request.user = self.user
        response = views.remove_baseline_item(request, 1, 1, 1, 1, 2)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
        
    def test_delete_baseline(self):
        ctx = {'id_user':1, 'id_project':1, 'id_phase':1, 'id_baseline':2}
        request = self.factory.get(reverse('delete_baseline', kwargs=ctx))
        request.user = self.user
        response = views.delete_baseline(request, 1, 1, 1, 2)
        self.assertEqual(response.status_code, 200, "No ha retornado la pagina")
