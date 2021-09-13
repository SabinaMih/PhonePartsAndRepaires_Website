import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest

class test_BookingAdminSearch(unittest.TestCase):
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
        # login as admin 
        if username.is_displayed() and user_password.is_displayed():
            username.send_keys("staff")
            user_password.send_keys("sdev2020" + Keys.RETURN)
        # go to admin interface page
        admin_menu_link = self.chrome_webbrowser.find_element_by_partial_link_text('WELCOME BACK, STAFF.')
        admin_menu_link.click()
        manage_bookings_link = self.chrome_webbrowser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/li/div/a[2]')
        manage_bookings_link.click()
        search_bookings_link = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/nav/ul/li[1]/a')
        search_bookings_link.click()
        #check title
        actual_title = self.chrome_webbrowser.title
        self.assertEquals(actual_title, "Search Bookings")

    def tearDown(self):
        # close the web browser
        self.chrome_webbrowser.close()
        print("Test script executed successfully.")
        time.sleep(4)
        self.chrome_webbrowser.quit()
    
    def test_search_by_email_admin_successfully(self):
        search_input = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/form/input[2]')
        search_input.send_keys('sab09@gmail.com' + Keys.RETURN)
        
        search_info = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/p[1]').text
        self.assertEquals(search_info, 'You have searched for: sab09@gmail.com')
        search_entry = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/span/a').text
        self.assertEquals(search_entry, 'sab09@gmail.com | iPhone 8 | Audio | Post |May 30, 2021')
    
    def test_search_by_email_no_results_admin_successful(self):
        search_input = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/form/input[2]')
        search_input.send_keys('test@gmail.com' + Keys.RETURN)
        search_info = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/p[1]').text
        self.assertEquals(search_info, 'You have searched for: test@gmail.com')
        no_results = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/p[2]').text
        self.assertEquals(no_results, 'No results found')
   #hr 
    def test_search_by_phone_model_admin_successfully(self):
        search_input = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/form/input[2]')
        search_input.send_keys('iPhone' + Keys.RETURN)
        
        search_info = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/p').text
        self.assertEquals(search_info, 'You have searched for: iPhone')
        search_entry = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/span/a').text
        self.assertEquals(search_entry, 'sab09@gmail.com | iPhone 8 | Audio | Post |May 30, 2021')
    
    def test_search_by_fault_admin_successfully(self):
        search_input = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/form/input[2]')
        search_input.send_keys('audio' + Keys.RETURN)
        
        search_info = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/p').text
        self.assertEquals(search_info, 'You have searched for: audio')
        search_entry = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/span/a').text
        self.assertEquals(search_entry, 'sab09@gmail.com | iPhone 8 | Audio | Post |May 30, 2021')

    def test_search_by_booking_type_admin_successfully(self):
        search_input = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/form/input[2]')
        search_input.send_keys('post' + Keys.RETURN)
        
        search_info = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/p').text
        self.assertEquals(search_info, 'You have searched for: post')
        search_entry = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/span/a').text
        self.assertEquals(search_entry, 'sab09@gmail.com | iPhone 8 | Audio | Post |May 30, 2021')
    
    
    def test_access_booking_from_search_results_admin_successful(self):
        search_input = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/form/input[2]')
        search_input.send_keys('sab09@gmail.com' + Keys.RETURN)
        search_entry = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div[2]/div[2]/div/span/a')
        # click on the booking
        self.chrome_webbrowser.execute_script("arguments[0].click()", search_entry)
        self.assertEquals(self.chrome_webbrowser.title, 'My Bookings')
        booking_email = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/span[6]').text
        self.assertEquals(booking_email, 'sab09@gmail.com')


    
    