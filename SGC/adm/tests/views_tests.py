from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from adm.models import Role
from adm.views import list_users_view, add_user_view, mod_user_view, del_user_view, user_role_view, list_role_view, grant_role_view, deny_role_view
from adm.views import all_roles_view, add_role_view, mod_role_view, del_role_view, role_permission_view, list_permission_view, grant_permission_view, deny_permission_view


class TestCase01(TestCase):    
    fixtures = ['users_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()        
        
    def test01_list_users_view(self):
        
        print "\n1) Listar usuarios\n"       
        request = self.factory.get('/adm/list_users/')        
        self.user = User.objects.get(pk=2)
        request.user = self.user        
        response = list_users_view(request)        
        print "  > Codigo de estado de la pagina obtenida: %s"%response.status_code
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.content)
        
    def test02_add_user_view(self):
        
        print "\n2) Crear usuario\n"        
        request = self.factory.get('/adm/add_user/')       
        self.user = User.objects.get(pk=2)
        request.user = self.user        
        response = add_user_view(request)        
        print "  > Codigo de estado de la pagina obtenida: %s"%response.status_code
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.content)
        
        print "  > Iniciamos sesion con la cuenta admin"
        self.client.login(username='admin', password='admin')
        
        print "  > Se cargan datos de un nuevo usuario en la direccion /adm/list_user/add_user/."
        print "  > Algunos de los datos enviados son: "
        print "    - username : carolina"
        print "     - password : carolina"
        print "     - ..."
        response = self.client.post('/adm/add_user/', {'username':'carolina','password':'carolina',
                                                       'firstName':'Carolina', 'lastName':'Arguello',
                                                       'email':'carolina@gmail.com', 'phonenum':'0',
                                                       'address':'', 'observation':''})
             
        print "  > Codigo de estado de la pagina obtenida: %s"%response.status_code
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/adm/list_users/')
        
        print "  > Se verifica que el usuario 'carolina' fue correctamente creado."
        user = User.objects.get(pk=5)
        print "    - username: %s"%user.username      
        print "    - email: %s"%user.email
        print "    - phonenum: %s"%user.phonenum
        
        self.assertTrue(user)
        
    def test03_mod_user_view(self):
        
        print "3) Modificar usuario\n"
        request = self.factory.get('/adm/mod_user/3/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = mod_user_view(request, 3)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.content)
        self.assertTrue('user' in response.content)
        
        self.client.login(username='admin', password='admin')
        
        response = self.client.post('/adm/mod_user/3/', {'username':'nobu','password':'nobu',
                                                       'firstName':'Nobuyoshi', 'lastName':'Ishii',
                                                       'email':'ishiiaquino@gmail.com', 'phonenum':'1', 'address':'1',
                                                       'observation':'abc'})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/adm/list_users/')
        
        firstName = User.objects.get(pk=3).firstName
        
        self.assertEqual(firstName, 'Nobuyoshi')
        
    def test04_del_user_view(self):
        
        print "4) Eliminar usuario\n"
        request = self.factory.get('/adm/del_user/3/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = del_user_view(request, 3)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.content)
        
        self.client.login(username='admin', password='admin')
        
        response = self.client.post('/adm/del_user/3/')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/adm/list_users/')
        
        user = User.objects.filter(pk=3)
        
        self.assertFalse(user)
        
    def test05_user_role_view(self):
        
        print "5) Roles del usuario\n"
        request = self.factory.get('/adm/user_role/2/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = user_role_view(request, 2)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.content)
        self.assertTrue('roles' in response.content)
        
    def test06_list_role_view(self):
        
        print "6) Listar roles disponibles para otorgar al usuario\n"
        request = self.factory.get('/adm/list_role/2/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = list_role_view(request, 2)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.content)
        self.assertTrue('roles' in response.content)
        
    def test07_grant_role_view(self):
        
        print "7) Otorgar rol al usuario\n"
        request = self.factory.get('/adm/grant_role/2/2/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = grant_role_view(request, 2, 2)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.content)
        self.assertTrue('role' in response.content)
        
        user = User.objects.get(pk=2)
        role = user.roles.filter(pk=2)
        
        self.assertTrue(role)
        
    def test08_deny_role_view(self):
        
        print "8) Desvincular rol del usuario\n"
        request = self.factory.get('/adm/deny_role/2/2/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = deny_role_view(request, 2, 2)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.content)
        self.assertTrue('role' in response.content)
        
        user = User.objects.get(pk=2)
        role = user.roles.filter(pk=2)
        
        self.assertFalse(role)
        
class TestCase02(TestCase):
    fixtures = ['users_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test01_all_roles_view(self):
        
        print "1) Listar todos los roles existentes\n"
        request = self.factory.get('/adm/all_roles/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = all_roles_view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('roles' in response.content)
        
    def test02_add_role_view(self):
        
        print "2) Crear rol\n"
        request = self.factory.get('/admi/add_role/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = add_role_view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.content)
        
        self.client.login(username='admin', password='admin')
        
        response = self.client.post('/adm/add_role/', {'name': 'Programador', 'description':'Posee permisos para modificar.'})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/adm/all_roles/')
        
        role = Role.objects.get(pk=3)
        
        self.assertTrue(role)
        
    def test03_mod_role_view(self):
        
        print "3) Modificar rol\n"
        request = self.factory.get('/adm/mod_role/2/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = mod_role_view(request, 2)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.content)
        self.assertTrue('rol' in response.content)
        
        self.client.login(username='admin', password='admin')
        
        response = self.client.post('/adm/mod_role/2/', {'name': 'Analista', 'description':'Posee permiso para visualizar.'})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/adm/all_roles/')
        
        roleName = Role.objects.get(pk=2).name
        
        self.assertEqual(roleName, 'Analista')
    
    def test04_del_role_view(self):
        
        print "4) Eliminar rol\n"
        request = self.factory.get('/adm/del_role/3/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = del_role_view(request, 2)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('role' in response.content)
        
        self.client.login(username='admin', password='admin')
        
        response = self.client.post('/adm/del_role/2/')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/adm/all_roles/')
        
        role = Role.objects.filter(pk=2)
        
        self.assertFalse(role)
    
    def test05_role_permission_view(self):
        
        print "5) Permisos del rol\n"
        request = self.factory.get('/adm/role_permission/2/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = role_permission_view(request, 2)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('role' in response.content)
        self.assertTrue('permission' in response.content)
    
    def test06_list_permission_view(self):
        
        print "6) Listar permisos disponibles para el rol\n"
        request = self.factory.get('/adm/list_permission/2/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = list_permission_view(request, 2)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('role' in response.content)
        self.assertTrue('permission' in response.content)
    
    def test07_grant_permission_view(self):
        
        print "7) Agregar permiso al rol\n"
        request = self.factory.get('/adm/grant_permission/2/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = grant_permission_view(request, 2, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('role' in response.content)
        self.assertTrue('permission' in response.content)
        
        role = Role.objects.get(pk=2)
        permission = role.permissions.filter(pk=1)
        
        self.assertTrue(permission)
    
    def test08_deny_permission_view(self):
        
        print "8) Quitar permiso del rol\n"
        request = self.factory.get('/adm/deny_permission/2/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = deny_permission_view(request, 2, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('role' in response.content)
        self.assertTrue('permission' in response.content)
        
        role = Role.objects.get(pk=2)
        permission = role.permissions.filter(pk=1)
        
        self.assertFalse(permission)
