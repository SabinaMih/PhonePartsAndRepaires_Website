import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest

class test_BookingDates(unittest.TestCase):
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
        if username.is_displayed() and user_password.is_displayed():
            username.send_keys("sabina")
            user_password.send_keys("sdev2020" + Keys.RETURN)
        

    def tearDown(self):
        # close the web browser
        self.chrome_webbrowser.close()
        print("Test script executed successfully.")
        time.sleep(4)
        self.chrome_webbrowser.quit()
        
    def test_fully_booked_msg_displyed_Succesful_inChrome(self):
        # go to booking form 
        booking_link = self.chrome_webbrowser.find_element_by_partial_link_text('BOOK A REPAIR')
        booking_link.click()
        # fill in the booking form, the shop takes only 5 bookings per day
        # when fully booked the user is notified to change the date 
        for booking in range(6):
            email = self.chrome_webbrowser.find_element_by_name('email')
            email.send_keys("sab09@gmail.com")
            phone = Select(self.chrome_webbrowser.find_element_by_name('phone'))
            phone.select_by_visible_text('iPhone 8')
            fault = Select(self.chrome_webbrowser.find_element_by_name('fault'))
            fault.select_by_visible_text('Audio')
            booking_type = Select(self.chrome_webbrowser.find_element_by_name('booking_type'))
            booking_type.select_by_visible_text('Post')
            comment = self.chrome_webbrowser.find_element_by_name('comment')
            comment.send_keys("Some comment")
            booking_date = self.chrome_webbrowser.find_element_by_xpath('//*[@id="id_booking_date"]')
            booking_date.send_keys("26052021")
            time.sleep(3)
            submit_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div/div[2]/form/button')
            self.chrome_webbrowser.execute_script("arguments[0].click()", submit_btn)
            if booking == 5:
                # check if the validation works
                expected_fully_booked_msg = "Fully booked please select a different day!"
                actual_fully_booked_msg = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div/div[2]/form/div[1]/ul/li').text
                self.assertEquals(expected_fully_booked_msg, actual_fully_booked_msg)
                booking_date = self.chrome_webbrowser.find_element_by_xpath('//*[@id="id_booking_date"]')
                booking_date.send_keys("27052021") #book a different day
                #submit again
                submit_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div/div[2]/form/button')
                self.chrome_webbrowser.execute_script("arguments[0].click()", submit_btn)
            
            home_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div/div/div/p[3]/a[2]')
            home_btn.click()
            booking_link = self.chrome_webbrowser.find_element_by_partial_link_text('BOOK A REPAIR')
            booking_link.click()
        
        def test_invalid_date_entered_by_user_returns_error_msg(self):
            email = self.chrome_webbrowser.find_element_by_name('email')
            email.send_keys("sab09@gmail.com")
            phone = Select(self.chrome_webbrowser.find_element_by_name('phone'))
            phone.select_by_visible_text('iPhone 8')
            fault = Select(self.chrome_webbrowser.find_element_by_name('fault'))
            fault.select_by_visible_text('Audio')
            booking_type = Select(self.chrome_webbrowser.find_element_by_name('booking_type'))
            booking_type.select_by_visible_text('Post')
            comment = self.chrome_webbrowser.find_element_by_name('comment')
            comment.send_keys("Some comment")
            booking_date = self.chrome_webbrowser.find_element_by_xpath('//*[@id="id_booking_date"]')
            booking_date.send_keys("26052020") #date in the past
            time.sleep(3)
            submit_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div/div[2]/form/button')
            self.chrome_webbrowser.execute_script("arguments[0].click()", submit_btn)
            #check if error message appears
            expected_error_msg = "Please select date in the future!"
            actual_error_msg = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div/div[2]/form/div[1]/ul/li').text
            self.assertEquals(expected_error_msg, actual_error_msg)
            booking_date = self.chrome_webbrowser.find_element_by_xpath('//*[@id="id_booking_date"]')
            booking_date.send_keys("29052021") #book a different day
            #submit again
            submit_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div/div[2]/form/button')
            self.chrome_webbrowser.execute_script("arguments[0].click()", submit_btn)

        

            
            
        

    
        



