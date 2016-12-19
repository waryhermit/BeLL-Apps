import unittest
import datetime
import bell

from base_case import on_platforms
from base_case import browsers
from base_case import BaseCase

from selenium import webdriver
from selenium.webdriver.remote import webelement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
@on_platforms(browsers)
class MeetupTest(BaseCase):
    """description of class"""
    # http://www.seleniumhq.org/docs/06_test_design_considerations.jsp#page-object-design-pattern
   
    def create_Member(self,driver):
        wait = WebDriverWait(driver, 25)
        bell.login(driver,"admin","password")
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID,'itemsinnavbar')))
        ele = driver.find_element_by_css_selector('a[href="#meetups"]')
        ele.click()
        ##driver.get("http://127.0.0.1:5981/apps/_design/bell/MyApp/index.html#meetups")
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID,'linkOfMeetUpHeading')))
        submit = wait.until(EC.element_to_be_clickable((By.ID,'linkOfMeetUpHeading')))
        ele = driver.find_element_by_css_selector('a[href="#meetup/add"]')
        print(submit.text)
        submit.send_keys(Keys.NULL)
        submit.send_keys(Keys.ENTER)
        submit.click()
        submit.click()
        submit.click()
        submit.click()
        submit.click()
        submit.click()
        ##submit.click()
       

        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID,'meetUpForm')))
        elem = driver.find_element_by_name("title")
        elem.send_keys("Test Meetup")
        elem = driver.find_element_by_name("description")
        elem.send_keys("This is a test meeting automatically created by test_meetup.py")
        elem = driver.find_element_by_name("startDate")
        elem.send_keys(datetime.datetime.now().strftime('%d/%m/%Y'))
        elem = driver.find_element_by_name("endDate")
        i = datetime.datetime.now() + datetime.timedelta(days=1)
        elem.send_keys(i.strftime('%d/%m/%Y'))

        elem = driver.find_element_by_name("startTime")
        elem.send_keys("8:00am")


        elem = driver.find_element_by_name("endTime")
        elem.send_keys("11:00pm")

        elem = driver.find_element_by_name("category")
        select = Select(elem)
        select.select_by_index(1)

        elem = driver.find_element_by_name("meetupLocation")
        elem.send_keys("Test catagory")
        submit = driver.find_element_by_id("MeetUpformButton")
        submit.click()
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID,'formButton')))


    def test_add_new_meetup(self):
        """ comment"""
        driver = self.driver
        self.create_Member(driver)

        submit = driver.find_element_by_id("formButton")
        submit.click()
        WebDriverWait(driver, 25).until(EC.alert_is_present())
        actual = Alert(driver).text
        expected = "Invitation sent successfully."
        self.assertEqual(actual, expected)
        Alert(driver).accept()
        

    def test_delete_meetup(self):
        """ comment"""
        driver = self.driver
        wait = WebDriverWait(driver, 25)
        bell.login(driver,"admin","password")
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID,'itemsinnavbar')))
        ele = driver.find_element_by_css_selector('a[href="#meetups"]')
        ele.click()
        submit = wait.until(EC.element_to_be_clickable((By.ID,'linkOfMeetUpHeading')))
        try:
            submit = driver.find_element_by_xpath("//*[@id='parentLibrary']/table/tbody/tr[2]/td[4]/a")
        except NoSuchElementException:
            self.assertFalse(True)
        exists = True
        while exists:
            try:
                submit = driver.find_element_by_xpath("//*[@id='parentLibrary']/table/tbody/tr[2]/td[4]/a")
                submit.click()
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                #actual = Alert(driver).text
                #expected = "Invitation sent successfully."
                #self.assertEqual(actual, expected)
                Alert(driver).accept()
            except (NoSuchElementException, TimeoutException) as e:
                exists = False
        
        self.assertTrue(True)

    def test_invite_member(self):
         driver = self.driver
         self.create_Member(self.driver)
         elem = driver.find_element_by_name("invitationType")
         select = Select(elem)
         select.select_by_index(1)

         WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.NAME,'members')))
         elem = driver.find_element_by_name("members")
         chkboxes = elem.find_elements_by_tag_name("input")
         for val in chkboxes:
            val.click()
         sleep(1)
         submit = driver.find_element_by_id("formButton")
         submit.click()
         WebDriverWait(driver, 25).until(EC.alert_is_present())
         actual = Alert(driver).text
         expected = "Invitation sent successfully."
         self.assertEqual(actual, expected)
         Alert(driver).accept()

    #def test_multiday_meetup(self):
    #    """ comment"""
    #def test_singleday_meetup(self):
    #    """ comment"""
    #def recurring_meetup(self):
    #    """ comment"""



    if __name__ == "__main__":
        unittest.main()