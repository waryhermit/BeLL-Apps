import unittest
import bell

from base_case import on_platforms
from base_case import browsers
from base_case import BaseCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

# NOTICE: This code is totally ugly and needs refactoring, but I'm 
#         just testing functionality before today's meeting.

@on_platforms(browsers)
class MemberTest(BaseCase):

    def test_add_member(self):
        driver = self.driver
        
        # data = birthdate, gender, level
        data = [["1", "11", "1924"], "Female", "4"]
        
        # adding new member
        # get to the form page
        self.setup()
        # fill up the form without uploading a file
        self.fill_form("a", data, True)
        #TODO: test new member login
        
        # adding already existing member
        # get back to the form page
        self.setup()
        # fill up the form without uploading a file
        self.fill_form("a", data)
        #TODO: test new member login

#        # adding new member and uploading file
#        # data = birthdate, gender, level
#        data = [["31", "0", "1934"], "Male", "Higher"]
#        # attachment = "" #TODO: insert filename
#        # get to the form page
#        self.setup()
#        # fill up the form uploading a file
#        self.fill_form("b", data, True, True, attachment)
        
        
    def setup(self):
        """ NoneType -> NoneType
        
        Go to the login page, click on Become a Member, and 
        test we're landing on the page to fill the form
        """
        driver = self.driver
        
        # go to the login page
        driver.get("http://127.0.0.1:5981/apps/_design/bell/MyApp/index.html")
        # click on become a member button
        button = driver.find_element_by_link_text("Become a Member")
        button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "memberform")))
        actual = driver.current_url
        expected = "http://127.0.0.1:5981/apps/_design/bell/MyApp/index.html#member/add"
        self.assertEqual(actual, expected)
    
    def fill_form(self, fill, data, new, upload=False, attachment=None):
        """ (string, list, bool, bool, string) -> string
        
        Helper function to fill out a new member's registration form.
        Takes one single string (fill) to fill out all the data except 
        for the dropdown options. Birthdate, gender, and levels are used 
        to fill out the dropdown option. 
        New determines whether or not we're filling the form for a new
        member. If the member is new, then successful registration is
        expected, otherwise we expect to find out that the member was 
        already registered.
        Upload determines whether or not a file needs to be uploaded. 
        If upload is True, then attachment is the file to be uploaded.
        Returns the text of the alert (either the member has been
        successfully registered or was already existing)
        """
        driver = self.driver
        
        # fill info form
        fields = ["firstName", "lastName", "middleNames", "login", "password", "phone", "email", "language"]
        for field in fields:
            elem = driver.find_element_by_name(field)
            elem.send_keys(fill)
        
        birthdate, gender, level = data
        
        # TODO: refactor to avoid repetition
        # select the birth date
        # day 
        dropdown = Select(driver.find_element_by_xpath("//*[contains(@id, 'BirthDate')]/select[1]"))
        dropdown.select_by_value(birthdate[0])
        # month
        dropdown = Select(driver.find_element_by_xpath("//*[contains(@id, 'BirthDate')]/select[2]"))
        dropdown.select_by_value(birthdate[1])
        # year
        dropdown = Select(driver.find_element_by_xpath("//*[contains(@id, 'BirthDate')]/select[3]"))
        dropdown.select_by_value(birthdate[2])
        
        # select the gender
        dropdown = Select(driver.find_element_by_xpath("//*[contains(@id, 'Gender')]"))
        dropdown.select_by_value(gender)
        
        # select the level
        dropdown = Select(driver.find_element_by_xpath("//*[contains(@id, 'levels')]"))
        dropdown.select_by_value(level)
        
        # TODO: add attachment, if present
        #if upload:
        #   #TODO: find element and attach file
              
        # submit the form
        button = driver.find_element_by_id("formButton")
        button.click()
        
        # read the alert
        actual = Alert(driver).text
        if new:
            expected = "Successfully registered."
        else:
            expected = "Login already exists."
        self.assertEqual(actual, expected)
        Alert(driver).accept()
        # test we're back to the login page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login")))
        actual = driver.current_url
        expected = "http://127.0.0.1:5981/apps/_design/bell/MyApp/index.html#login"
        self.assertEqual(actual, expected)
        #TODO: login and test if attachment uploaded correctly
        

if __name__ == "__main__":
    unittest.main()
