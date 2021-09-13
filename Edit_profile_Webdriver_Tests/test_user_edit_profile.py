import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest

class test_UserEditProfile(unittest.TestCase):
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
        # login as user
        login_link = self.chrome_webbrowser.find_element_by_partial_link_text('SIGN IN/REGISTER')
        login_link.click()
        username = self.chrome_webbrowser.find_element_by_name('username')
        username.clear()
        username.send_keys("sabina")
        user_password = self.chrome_webbrowser.find_element_by_name('password') 
        user_password.clear()
        user_password.send_keys("sdev2020" + Keys.RETURN)

        menu_link = self.chrome_webbrowser.find_element_by_xpath('//*[@id="navbarDropdown"]')
        self.chrome_webbrowser.execute_script("arguments[0].click()", menu_link)
        # go to edit profile page
        profile_link = self.chrome_webbrowser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/li/div/a[2]')
        self.chrome_webbrowser.execute_script("arguments[0].click()", profile_link)

        if self.chrome_webbrowser.current_url != "http://127.0.0.1:8000/edit_profile/":
            print("Wrong page loaded")
        
        
    def tearDown(self):
        # close the web browser
        self.chrome_webbrowser.close()
        print("Test script executed successfully.")
        time.sleep(4)
        self.chrome_webbrowser.quit()
        
    def test_user_edit_profile_Succesful(self):
        # verify title
        expected_title = "Edit Profile"
        actual_title = self.chrome_webbrowser.title
        if expected_title != actual_title:
            print("Verification Failed - An incorrect title is displayed on the web page: " + actual_title )
        self.assertEquals(expected_title, actual_title)

        # fill in the edit form and submit
        username = self.chrome_webbrowser.find_element_by_name('username')
        username.clear()
        username.send_keys("newusername")
        email = self.chrome_webbrowser.find_element_by_name('email')
        email.clear()
        email.send_keys("newsab09@gmail.com")
        first_name = self.chrome_webbrowser.find_element_by_name('first_name')
        first_name.clear()
        first_name.send_keys('Sabina')
        last_name = self.chrome_webbrowser.find_element_by_name('last_name')
        last_name.clear()
        last_name.send_keys('Mihoc')
        delete_account = self.chrome_webbrowser.find_element_by_name('delete_profile')
        delete_account.send_keys(True)
        update_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div/div[2]/form/p[4]/button')
        self.chrome_webbrowser.execute_script("arguments[0].click()", update_btn)
        time.sleep(3)
        #check redirect to home page
        expected_title = "See Our Products & Services"
        actual_title = self.chrome_webbrowser.title
        if expected_title != actual_title:
            print("Verification Failed" + actual_title )
        self.assertEquals(expected_title, actual_title)
        #check new user name display on the menu
        expected_user_name = "WELCOME BACK, NEWUSERNAME."
        actual_user_name = self.chrome_webbrowser.find_element_by_partial_link_text('NEWUSERNAME.').text
        if expected_user_name != actual_user_name:
            print("Verification Failed - An incorrect user name is displayed on the web page: " + actual_user_name )
        self.assertEquals(expected_user_name, actual_user_name)

        # change the user name with the previous 
        menu_link = self.chrome_webbrowser.find_element_by_xpath('//*[@id="navbarDropdown"]')
        self.chrome_webbrowser.execute_script("arguments[0].click()", menu_link)
        # go to edit profile page
        profile_link = self.chrome_webbrowser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/li/div/a[2]')
        self.chrome_webbrowser.execute_script("arguments[0].click()", profile_link)
        username = self.chrome_webbrowser.find_element_by_name('username')
        username.clear()
        username.send_keys("sabina")
        update_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div/div[2]/form/p[4]/button')
        self.chrome_webbrowser.execute_script("arguments[0].click()", update_btn)



    def test_user_edit_profile_empty_field_fail(self):
        # fill in the edit form and submit
        username = self.chrome_webbrowser.find_element_by_name('username')
        username.clear()
        username.send_keys("")  #invalid
        email = self.chrome_webbrowser.find_element_by_name('email')
        email.clear()
        email.send_keys("")   #invalid
        first_name = self.chrome_webbrowser.find_element_by_name('first_name')
        first_name.clear()
        first_name.send_keys('Sabina')
        last_name = self.chrome_webbrowser.find_element_by_name('last_name')
        last_name.clear()
        last_name.send_keys('Mihoc')
        delete_account = self.chrome_webbrowser.find_element_by_name('delete_profile')
        delete_account.send_keys(True)
        update_btn = self.chrome_webbrowser.find_element_by_xpath('/html/body/nav[2]/div[2]/div/div[2]/form/p[4]/button')
        self.chrome_webbrowser.execute_script("arguments[0].click()", update_btn)
        time.sleep(3)
        #check if still on the same page because form is invalid
        expected_title = "Edit Profile"
        actual_title = self.chrome_webbrowser.title
        if expected_title != actual_title:
            print("Verification Failed" + actual_title )
        self.assertEquals(expected_title, actual_title)

        # go to home page
        self.app_url = "http://127.0.0.1:8000/"
        self.chrome_webbrowser.get(self.app_url)

        #check if the details are same as before
        expected_user_name = "WELCOME BACK, SABINA."
        actual_user_name = self.chrome_webbrowser.find_element_by_partial_link_text('SABINA.').text
        if expected_user_name != actual_user_name:
            print("Verification Failed - An incorrect user name is displayed on the web page: " + actual_user_name )
        self.assertEquals(expected_user_name, actual_user_name)
