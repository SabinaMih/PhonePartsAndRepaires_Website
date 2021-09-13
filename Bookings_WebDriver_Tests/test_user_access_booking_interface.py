import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class test_UserAccessForbidden(unittest.TestCase):
    chrome_webbrowser = ""
    app_url = ""
    
    def setUp(self):
        self.chrome_webbrowser = webdriver.Chrome("Bookings_WebDriver_Tests\chromedriver.exe")
        #get the html
        self.app_url = "http://127.0.0.1:8000/login/"
        self.chrome_webbrowser.get(self.app_url)
        self.chrome_webbrowser.maximize_window()
        self.chrome_webbrowser.implicitly_wait(3)
        username = self.chrome_webbrowser.find_element_by_name('username')
        username.clear()
        user_password = self.chrome_webbrowser.find_element_by_name('password') 
        user_password.clear()
        # login as user
        if username.is_displayed() and user_password.is_displayed():
            username.send_keys("sabina")
            user_password.send_keys("sdev2020" + Keys.RETURN)
        user_menu_link = self.chrome_webbrowser.find_element_by_partial_link_text('WELCOME BACK, SABINA.')
        user_menu_link.click()
        
    def tearDown(self):
        # close the web browser
        self.chrome_webbrowser.close()
        print("Test script executed successfully.")
        time.sleep(4)
        self.chrome_webbrowser.quit()
    
    def test_user_access_manage_bookings_page_forbidden(self):
        self.manage_bookings_url = 'http://127.0.0.1:8000/booking/manageBookings/'
        self.chrome_webbrowser.get(self.manage_bookings_url)
        expected_forbidden = '403 Forbidden'
        actual = self.chrome_webbrowser.find_element_by_xpath('/html/body/h1').text
        self.assertEqual(expected_forbidden, actual)
    
    def test_user_access_add_phone_page_forbidden(self):
        self.add_phone_url = 'http://127.0.0.1:8000/booking/phoneNew/'
        self.chrome_webbrowser.get(self.add_phone_url)
        expected_forbidden = '403 Forbidden'
        actual = self.chrome_webbrowser.find_element_by_xpath('/html/body/h1').text
        self.assertEqual(expected_forbidden, actual)
    
    def test_user_access_add_fault_page_forbidden(self):
        self.add_type_url = 'http://127.0.0.1:8000/booking/newBookingType/'
        self.chrome_webbrowser.get(self.add_type_url)
        expected_forbidden = '403 Forbidden'
        actual = self.chrome_webbrowser.find_element_by_xpath('/html/body/h1').text
        self.assertEqual(expected_forbidden, actual)
    
    
    def test_user_access_add_booking_type_page_forbidden(self):
        self.add_fault_url = 'http://127.0.0.1:8000/booking/newFault/'
        self.chrome_webbrowser.get(self.add_fault_url)
        expected_forbidden = '403 Forbidden'
        actual = self.chrome_webbrowser.find_element_by_xpath('/html/body/h1').text
        self.assertEqual(expected_forbidden, actual)


    def test_user_access_search_bookings_page_forbidden(self):
        self.search_bookings_url = 'http://127.0.0.1:8000/booking/bookingSearch/'
        self.chrome_webbrowser.get(self.search_bookings_url)
        expected_link = 'http://127.0.0.1:8000/admin/login/?next=/booking/bookingSearch/'  # redirect to admin login
        self.assertEqual(self.chrome_webbrowser.current_url, expected_link)
