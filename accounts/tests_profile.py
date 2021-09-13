from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from accounts.models import CustomUser
from django.urls import reverse


class AccountsTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='sabinamihoc02@gmail.com',
            password='secret'
        )

    #def tearDown(self):
        #self.user.delete()

    def test_user_login_correct_credentials(self):
        self.user = authenticate(username='testuser', password='secret')
        self.assertTrue((self.user is not None) and self.user.is_authenticated)
        login = self.client.login(username='testuser', password='secret')
        self.assertTrue(login)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
    
    def test_user_details_before_update_correct(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'sabinamihoc02@gmail.com')
        self.assertEqual(self.user.first_name, '')
        self.assertEqual(self.user.last_name, '')
       
    
    def test_edit_profile_form_as_user_successfully(self):
        login = self.client.login(username='testuser', password='secret')
        self.assertTrue(login)
        response = self.client.get('/edit_profile/')
        self.assertEqual(response.status_code, 200)  #ok
        #fill in the form
        response=self.client.post(reverse('accounts:edit_profile'), data={'username':'sabina',
                                                                          'email':'otheremail@gmail.com',
                                                                          'first_name':'Sabina',
                                                                          'last_name':'Mihoc',
                                                                          'delete_profile':True})
        self.assertEqual(response.status_code, 302) # page is moved temporarily. 
        # check if after update button is pressed the home page is displayed
        response=self.client.get(reverse('shop:allProdCat'))
        self.assertEqual(response.status_code, 200)
        # login with new credentials
        login = self.client.login(username='sabina', password='secret')
        self.assertTrue(login) #true
    
    def test_edit_profile_form_empty_fields_as_user_fail(self):
        login = self.client.login(username='testuser', password='secret')
        self.assertTrue(login)
        response = self.client.get('/edit_profile/')
        self.assertEqual(response.status_code, 200)  #ok
        #fill in the form
        response=self.client.post(reverse('accounts:edit_profile'), data={'username':'',
                                                                          'email':'',
                                                                          'first_name':'',
                                                                          'last_name':'',
                                                                          'delete_profile':False})
        self.assertEqual(response.status_code, 200)  # OK status, page is not moved
        # login invalid
        login = self.client.login(username='', password='secret')
        self.assertFalse(login)     # no login
       