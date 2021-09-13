import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest

class test_BookingAdminCrud(unittest.TestCase):
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
        #check title
        actual_title = self.chrome_webbrowser.title
        self.assertEquals(actual_title, "Manage Bookings")

    def tearDown(self):
        # close the web browser
        self.chrome_webbrowser.close()
        print("Test script executed successfully.")
        time.sleep(4)
        self.chrome_webbrowser.quit()
    
    def test_add_phone_admin_successfull(self):
        phones_link = self.chrome_webbrowser.find_element_by_partial_link_text('PHONES')
        phones_link.click()
        #check url
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/model/')
        #check title
        self.assertEquals(self.chrome_webbrowser.title, "Phone Models")
        add_phones_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/p/a[1]')
        self.chrome_webbrowser.execute_script("arguments[0].click()", add_phones_btn)
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/phoneNew/')
        #check title
        self.assertEquals(self.chrome_webbrowser.title, "Add new phone")
        phone_input = self.chrome_webbrowser.find_element_by_name('phone')
        phone_input.send_keys("test phone model")
        submit_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/form/button')
        self.chrome_webbrowser.execute_script("arguments[0].click()", submit_btn)
        # check url after submit
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/model/')
        #check if phone is in the list
        time.sleep(4)
        phone_in_list = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr[14]/td[1]').text
        self.assertEquals(phone_in_list, "test phone model")

    def test_add_phone_empty_field_admin_fail(self):
        phones_link = self.chrome_webbrowser.find_element_by_partial_link_text('PHONES')
        phones_link.click()
        #check url
        add_phones_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/p/a[1]')
        self.chrome_webbrowser.execute_script("arguments[0].click()", add_phones_btn)
        phone_input = self.chrome_webbrowser.find_element_by_name('phone')
        phone_input.send_keys("")
        submit_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/form/button')
        self.chrome_webbrowser.execute_script("arguments[0].click()", submit_btn)
        # check url should be same page the form is not submitted
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/phoneNew/')

    def test_delete_phone_admin_successfull(self):
        phones_link = self.chrome_webbrowser.find_element_by_partial_link_text('PHONES')
        phones_link.click()
        # click on delete icone
        phone_in_list = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr[14]/td[1]').text
        if phone_in_list:
            self.assertEquals(phone_in_list, "test phone model")
            delete_icon = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr[14]/td[2]/p/a/i')
            self.chrome_webbrowser.execute_script("arguments[0].click()", delete_icon)
            time.sleep(4)
            print("The phone model was successfully deleted from the list.")

    def test_add_fault_admin_successfull(self):
        faults_link = self.chrome_webbrowser.find_element_by_partial_link_text('FAULTS')
        faults_link.click()
        #check url
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/faults/')
        #check title
        self.assertEquals(self.chrome_webbrowser.title, "Faults")
        add_fault_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/p/a[1]')
        self.chrome_webbrowser.execute_script("arguments[0].click()", add_fault_btn)
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/newFault/')
        #check title
        self.assertEquals(self.chrome_webbrowser.title, "Add new fault")
        fault_input = self.chrome_webbrowser.find_element_by_name('fault')
        fault_input.send_keys("test fault")
        cost_input = self.chrome_webbrowser.find_element_by_name('cost')
        cost_input.send_keys("10")
        submit_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/form/button')
        self.chrome_webbrowser.execute_script("arguments[0].click()", submit_btn)
        # check url after submit
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/faults/')
        #check if phone is in the list
        time.sleep(4)
        fault_in_list = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr[9]/td[1]').text
        self.assertEquals(fault_in_list, "test fault")
        cost_in_list = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr[9]/td[2]').text
        self.assertEquals(cost_in_list, "10.00")
    
    def test_add_fault_empty_field_admin_fail(self):
        faults_link = self.chrome_webbrowser.find_element_by_partial_link_text('FAULTS')
        faults_link.click()
        add_fault_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/p/a[1]')
        self.chrome_webbrowser.execute_script("arguments[0].click()", add_fault_btn)
        fault_input = self.chrome_webbrowser.find_element_by_name('fault')
        fault_input.send_keys("")
        cost_input = self.chrome_webbrowser.find_element_by_name('cost')
        cost_input.send_keys("")
        submit_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/form/button')
        self.chrome_webbrowser.execute_script("arguments[0].click()", submit_btn)
        # check url should be same the form is not subbmitted
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/newFault/')
        

    def test_delete_fault_admin_successfull(self):
        faults_link = self.chrome_webbrowser.find_element_by_partial_link_text('FAULTS')
        faults_link.click()
        # click on delete icone
        fault_in_list = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr[9]/td[1]').text
        if fault_in_list:
            self.assertEquals(fault_in_list, "test fault")
            delete_icon = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr[9]/td[3]/p/a/i')
            self.chrome_webbrowser.execute_script("arguments[0].click()", delete_icon)
            time.sleep(4)
            print("The fault was successfully deleted from the list.")
        
    def test_add_booking_type_admin_successfull(self):
        type_link = self.chrome_webbrowser.find_element_by_partial_link_text('BOOKING TYPES')
        type_link.click()
        #check url
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/bookingType/')
        #check title
        self.assertEquals(self.chrome_webbrowser.title, "Booking types")
        add_type_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/p/a[1]')
        self.chrome_webbrowser.execute_script("arguments[0].click()", add_type_btn)
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/newBookingType/')
        #check title
        self.assertEquals(self.chrome_webbrowser.title, "Add new booking type")
        type_input = self.chrome_webbrowser.find_element_by_name('booking_type')
        type_input.send_keys("test booking type")
        submit_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/form/button')
        self.chrome_webbrowser.execute_script("arguments[0].click()", submit_btn)
        # check url after submit
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/bookingType/')
        #check if boking type is in the list
        time.sleep(4)
        type_in_list = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr[3]/td[1]').text
        self.assertEquals(type_in_list, "test booking type")
    

    def test_add_booking_type_empty_field_admin_fail(self):
        type_link = self.chrome_webbrowser.find_element_by_partial_link_text('BOOKING TYPES')
        type_link.click()
        add_type_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/p/a[1]')
        self.chrome_webbrowser.execute_script("arguments[0].click()", add_type_btn)
        type_input = self.chrome_webbrowser.find_element_by_name('booking_type')
        type_input.send_keys("")
        submit_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/form/button')
        self.chrome_webbrowser.execute_script("arguments[0].click()", submit_btn)
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/newBookingType/')

    
    def test_delete_booking_type_admin_successfull(self):
        type_link = self.chrome_webbrowser.find_element_by_partial_link_text('BOOKING TYPES')
        type_link.click()
        # click on delete icone
        type_in_list = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr[3]/td[1]').text
        if type_in_list:
            self.assertEquals(type_in_list, "test booking type")
            delete_icon = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr[3]/td[2]/p/a')
            self.chrome_webbrowser.execute_script("arguments[0].click()", delete_icon)
            time.sleep(4)
            print("The booking type was successfully deleted from the list.")




        