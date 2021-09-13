import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest

class test_BookingDetails(unittest.TestCase):
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
        # go to booking details page
        menu_link = self.chrome_webbrowser.find_element_by_partial_link_text('WELCOME BACK, SABINA.')
        menu_link.click()
        # display the list with all the booking for the user
        my_bookings_link = self.chrome_webbrowser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/li/div/a[1]')
        my_bookings_link.click()

    def tearDown(self):
        # close the web browser
        self.chrome_webbrowser.close() 
        print("Test script executed successfully.")
        time.sleep(4)
        self.chrome_webbrowser.quit()
        
    def test_all_bookings_table_display_for_user_successful(self):
        # verify title
        expected_title = "My Bookings"
        actual_title = self.chrome_webbrowser.title
        if expected_title != actual_title:
            print("Verification Failed - An incorrect title is displayed on the web page: " + actual_title )
        self.assertEquals(expected_title, actual_title)
        # check if the booking datails appears on the table
        name=self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr/td[1]').text
        self.assertEquals(name, 'sabina')
        phone_model =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr/td[2]').text
        self.assertEquals(phone_model, 'iPhone 8')
        fault =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr/td[3]').text
        self.assertEquals(fault, 'Audio')
        booking_date =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr/td[4]').text
        self.assertEquals(booking_date, 'May 30, 2021')
        booking_type =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr/td[5]').text
        self.assertEquals(booking_type, 'Post')
        more =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr/td[6]/a').text
        self.assertEquals(more, 'See More')
    
    def test_booking_details_for_user_successfully(self):
        see_more_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr/td[6]/a')
        assert see_more_btn.is_displayed
        see_more_btn.click()
        header = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[1]/h4').text
        self.assertEquals(header, 'Booking Details')
        # check if the full booking datails appears on the page
        name=self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/span[2]').text
        self.assertEquals(name, 'sabina')
        phone_model =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/span[4]').text
        self.assertEquals(phone_model, 'iPhone 8')
        email_address =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/span[6]').text
        self.assertEquals(email_address, 'sab09@gmail.com')
        fault =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/span[8]').text
        self.assertEquals(fault, 'Audio')
        repair_cost =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/span[10]').text
        self.assertEquals(repair_cost, '€35.00')
        #date_created =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/span[14]').text
        #self.assertEquals(date_created, 'April 17, 2021')
        booking_date =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/span[16]').text
        self.assertEquals(booking_date, 'May 30, 2021')
        comment =self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/span[18]').text
        self.assertEquals(comment, 'Some comment')
        
        #check headers
        progress_bar_header = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[3]/h4[1]').text
        self.assertEquals(progress_bar_header, 'Progress')
        info_header = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[3]/h4[2]').text
        self.assertEquals(info_header, 'Info')
        #check progress bar disply
        progress_bar = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[3]/div/div')
        assert progress_bar.is_displayed
        #check if the buttons are displyed
        contactUs_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/p/a[3]')
        assert contactUs_btn.is_displayed
        home_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/p/a[1]')
        assert home_btn.is_displayed 
    
    def test_cancel_booking_user_successfully(self):
        #go to the booking details
        see_more_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr/td[6]/a')
        assert see_more_btn.is_displayed
        see_more_btn.click()
        #click on the cancel button
        cancel_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/p/a[2]')
        assert cancel_btn.is_displayed
        self.chrome_webbrowser.execute_script("arguments[0].click()", cancel_btn)
        self.assertEquals(self.chrome_webbrowser.title, 'Cancel Booking')
        expected_cancel_msg = "Are you sure you want to cancel you booking repair for iPhone 8 on May 30, 2021?"
        actual_cancel_msg = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/form/p[1]').text
        self.assertEquals(actual_cancel_msg, expected_cancel_msg)
        #check buttons
        back_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/form/p[2]/a')
        assert back_btn.is_displayed
        confirm_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[2]/form/p[2]/button')
        assert confirm_btn.is_displayed
        #click on confirm btn to cancel the booking
        self.chrome_webbrowser.execute_script("arguments[0].click()", confirm_btn)
        #check if cancel confirmation message is displyed
        expected_confirmation_msg = "Your booking was canceled."
        actual_confirmation_msg = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/h5').text
        self.assertEquals(actual_confirmation_msg, expected_confirmation_msg)
        # check if the url is correct
        self.assertEquals(self.chrome_webbrowser.current_url, 'http://127.0.0.1:8000/booking/all_bookings/')

    def test_booking_progress_bar_disply_user_successfully(self):
        #check header
        see_more_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/table/tbody/tr/td[6]/a')
        assert see_more_btn.is_displayed
        see_more_btn.click()
        expected_header = "Progress"
        actual_header = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[3]/h4[1] ').text
        self.assertEquals(expected_header, actual_header)
        # check progress bar
        actual_approved_status = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[3]/div/div[1]').text
        self.assertEquals(actual_approved_status, 'Booking Approved')
        actual_received_status = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[3]/div/div[2]').text
        self.assertEquals(actual_received_status, 'Device received')
        actual_repaired_status = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[3]/div/div[3]').text
        self.assertEquals(actual_repaired_status, 'Repaired')
        actual_collected_status = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[3]/div/div[4]').text
        self.assertEquals(actual_collected_status, 'Ready for collection')

        # check info message displyed
        actual_message = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div[1]/div/div[3]/p').text
        self.assertEquals(actual_message, 'Your Device is repaired. Please contact the shop to arrange a collection.')












