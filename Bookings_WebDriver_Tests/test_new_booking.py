import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest

class test_UserBooking(unittest.TestCase):
    chrome_webbrowser = ""
    app_url = ""
    
    def setUp(self):
        self.chrome_webbrowser = webdriver.Chrome("Bookings_WebDriver_Tests\chromedriver.exe")
        #get the html
        self.app_url = "http://127.0.0.1:8000/"
        # launch the chrome browser and open the application url
        self.chrome_webbrowser.get(self.app_url)
        # maximize the browser window
        self.chrome_webbrowser.maximize_window()
        self.chrome_webbrowser.implicitly_wait(3)

    def tearDown(self):
        # close the web browser
        self.chrome_webbrowser.close()
        print("Test script executed successfully.")
        time.sleep(4)
        self.chrome_webbrowser.quit()
        
    def test_user_creates_new_booking_Succesful_inChrome(self):
        login_link = self.chrome_webbrowser.find_element_by_partial_link_text('SIGN IN/REGISTER')
        login_link.click()

        if self.chrome_webbrowser.current_url != "http://127.0.0.1:8000/login/":
            print("Wrong page loaded")
        
        username = self.chrome_webbrowser.find_element_by_name('username')
        username.clear()
        user_password = self.chrome_webbrowser.find_element_by_name('password') 
        user_password.clear()
        if username.is_displayed() and user_password.is_displayed():
            # enter user details
            username.send_keys("sabina")
            user_password.send_keys("sdev2020" + Keys.RETURN)
        
        # verify if user name is displayed
        time.sleep(6)
        expected_user_name = "WELCOME BACK, SABINA."
        actual_user_name = self.chrome_webbrowser.find_element_by_partial_link_text('SABINA.').text
        if expected_user_name != actual_user_name:
            print("Verification Failed - An incorrect user name is displayed on the web page: " + actual_user_name )
        self.assertEquals(expected_user_name, actual_user_name)
        
        # go to booking form 
        booking_link = self.chrome_webbrowser.find_element_by_partial_link_text('BOOK A REPAIR')
        booking_link.click()

        if self.chrome_webbrowser.current_url != "http://127.0.0.1:8000/booking/newbooking/":
            print("Wrong page loaded")
        
        # verify title
        expected_title = "Book a repair"
        actual_title = self.chrome_webbrowser.title
        if expected_title != actual_title:
            print("Verification Failed - An incorrect title is displayed on the web page: " + actual_title )
        self.assertEquals(expected_title, actual_title)
        
        # fill in the booking form and submit
        email = self.chrome_webbrowser.find_element_by_name('email')
        email.send_keys("sab09@gmail.com")
        phone = Select(self.chrome_webbrowser.find_element_by_name('phone'))
        phone.select_by_visible_text('iPhone 8')
        fault = Select(self.chrome_webbrowser.find_element_by_name('fault'))
        fault.select_by_visible_text('Audio')
    
        booking_type = Select(self.chrome_webbrowser.find_element_by_name('booking_type'))
        booking_type.select_by_visible_text('Post')

        booking_date = self.chrome_webbrowser.find_element_by_xpath('//*[@id="id_booking_date"]')
        booking_date.send_keys("30052021")

        comment = self.chrome_webbrowser.find_element_by_name('comment')
        comment.send_keys("Some comment")
        submit_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div/div[2]/form/button')
        self.chrome_webbrowser.execute_script("arguments[0].click()", submit_btn)
        time.sleep(3)
        #check confirmation page displyed
        expected_title = "Confirmation"
        actual_title = self.chrome_webbrowser.title
        if expected_title != actual_title:
            print("Verification Failed - confirmation page not displayed" + actual_title )
        self.assertEquals(expected_title, actual_title)
        expected_confirmation_msg = "We received your booking request"
        actual_confirmation_msg = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div/div/div/p[1]').text
        self.assertEquals(expected_confirmation_msg, actual_confirmation_msg)
        expected_cost = "The estimated cost for repair is: €35.00"
        actual_cost = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div/div/div/p[2]').text
        # check if "My bookings" button is present
        my_bookings_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div/div/div/p[3]/a[1]')
        if my_bookings_btn.is_displayed == False:                
            print("Button is not displyed")
        assert my_bookings_btn.is_displayed
        #cancel_btn = self.chrome_webbrowser.find_element_by_link_text('Cancel').click()

    
        
 


