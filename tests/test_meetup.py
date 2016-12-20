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

from time import sleep

@on_platforms(browsers)
class MeetupTest(BaseCase):
   
    def create_Meetup(self,driver, numdays, cancel=False, recurring=False):
        wait = WebDriverWait(driver, 30)
        bell.login(driver,"admin","password")
        self.assertTrue(self.go_to_meetups(driver))

        # Make sure the'Add Meetup' button is there and press it. Keep clicking the button till its gone.
        addMeetupBtn = wait.until(EC.element_to_be_clickable((By.ID,'linkOfMeetUpHeading')))

        keepclicking = True
        while (keepclicking):
            try:
                addMeetupBtn.click()
                sleep(1)
            except:
                keepclicking = False

        # Wait for the form to appear and fill it out.
        wait.until(EC.presence_of_element_located((By.ID,'meetUpForm')))
        wait.until(EC.element_to_be_clickable((By.NAME,'title')))
        
        elem = driver.find_element_by_name("title")
        elem.send_keys("test_meetup.py - Test Meetup")
        elem = driver.find_element_by_name("description")
        elem.send_keys("This is a test meeting automatically created by test_meetup.py")
        elem = driver.find_element_by_name("startDate")
        elem.send_keys(datetime.datetime.now().strftime('%m/%d/%Y'))
        elem = driver.find_element_by_name("endDate")
        endDate = datetime.datetime.now() + datetime.timedelta(days=numdays)
        elem.send_keys(endDate.strftime('%m/%d/%Y'))

        elem = driver.find_element_by_name("startTime")
        elem.send_keys("8:00am")
        elem = driver.find_element_by_name("endTime")
        elem.send_keys("11:00pm")

        elem = driver.find_element_by_name("category")
        wait.until(EC.element_to_be_clickable((By.NAME,'category')))
        select = Select(elem)
        select.select_by_value('E Learning')

        elem = driver.find_element_by_name("meetupLocation")
        elem.send_keys("Test catagory")
        if (recurring):
            recurring_radio = driver.find_element_by_css_selector('input[type="radio"]')
            recurring_radio.click()
            WebDriverWait(driver, 25).until(EC.element_located_to_be_selected((By.ID, recurring_radio.get_attribute("id"))))

        if (cancel == False):
            # Bring up the invite page, since this is a new meetup.
            submit = driver.find_element_by_id("MeetUpformButton")
            submit.click()
            wait.until(EC.presence_of_element_located((By.ID,'formButton')))
        return True
    def go_to_meetups(self, driver):
        wait = WebDriverWait(driver, 15)
         # Go to the meetups tab
        wait.until(EC.element_to_be_clickable((By.ID,'itemsinnavbar')))
        old_page = driver.find_element_by_id('dashboard')
        meetups_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a[href="#meetups"]')))
        meetups_tab.click()

        # Clicking on the meetups link doesn't always work, so keep trying until we are at the meetups page.
        # This might only be needed due to a bug in the site see: https://github.com/open-learning-exchange/BeLL-Apps/issues/585
        keeptrying = True
        numoftries = 0
        while (keeptrying):
            try:
                # If the old page is stale then we are on the meetups tab.
                wait.until(EC.staleness_of(old_page))
                keeptrying = False
            except TimeoutException:
                meetups_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a[href="#meetups"]')))
                meetups_tab.click()
                numoftrys = numoftries + 1
                if (numoftries == 4):
                    # If we still haven't got there something else went wrong.
                    keeptrying = False
                    return False

        wait.until(EC.presence_of_element_located((By.ID,'linkOfMeetUpHeading')))
        return True

    def save_meetup(self, driver):
        try:
            submit = driver.find_element_by_id("formButton")
            submit.click()
        except (TimeoutException, NoSuchElementException) as e:
            print("Could not submit invatations. Check that you navigated to the invation screen and that formButton exists.")
            return False
        
        WebDriverWait(driver, 25).until(EC.alert_is_present())
        actual = Alert(driver).text
        expected = "Invitation sent successfully."
        Alert(driver).accept()
        return (actual == expected)    

    def test_add_new_meetup_singleday(self):
        driver = self.driver
        self.create_Meetup(driver, 1)
        self.assertTrue(self.save_meetup(driver))
        
    def test_delete_meetup(self):
        driver = self.driver
        wait = WebDriverWait(driver, 25)
        bell.login(driver,"admin","password")
        self.assertTrue(self.go_to_meetups(driver))

        # Check if there is at least one row of meetups.
        try:
            submit = driver.find_element_by_xpath("//*[@id='parentLibrary']/table/tbody/tr[2]/td[4]/a")
        except NoSuchElementException:
            self.assertFalse(True) # Nothing to delete.
        
        # Delete any meetups made by test_meetup.py
        meetups = driver.find_elements_by_xpath("//*[@id='parentLibrary']/table/tbody/tr[contains(.,'test_meetup.py')]/td/a[@class='destroy btn btn-danger']")
        deleted = False
        attempts = 0
        while (len(meetups) > 0):
            try:
                meetups[0].click()
                wait.until(EC.alert_is_present())
                Alert(driver).accept()
                wait.until(EC.staleness_of(meetups[0]))
                # Reload list -- the list is stale now that we deleted one.
                meetups = driver.find_elements_by_xpath("//*[@id='parentLibrary']/table/tbody/tr[contains(.,'Test')]/td/a[@class='destroy btn btn-danger']")
                deleted = True
            except:
                attempts = attempts + 1
                if (attempts > 5):
                    deleted = False
                    break

        self.assertTrue(deleted)

    def test_invite_member(self):
         driver = self.driver
         wait = WebDriverWait(driver, 15)
         self.create_Meetup(self.driver,1)
         elem = driver.find_element_by_name("invitationType")
         wait.until(EC.element_to_be_clickable((By.NAME,'invitationType')))

         invitationType = Select(elem)
         
         for opt in invitationType.options:
             print(str(opt))

         invitationType.select_by_index(1)


         wait.until(EC.presence_of_element_located((By.NAME,'members')))
         members_list = driver.find_element_by_name('members')
         chkboxes = members_list.find_elements_by_tag_name("input")

         for val in chkboxes:
            val.click()
         
         sleep(1)
         self.assertTrue(self.save_meetup(driver))

    def test_multiday_meetup(self):
        driver = self.driver
        self.create_Meetup(driver,3)
        self.assertTrue(self.save_meetup(driver))

    def test_recurring_meetup(self):
        driver = self.driver
        self.assertTrue(self.create_Meetup(self.driver,1,recurring=True))
        self.assertTrue(self.save_meetup(driver))

    def test_cancel_meetup(self):
        driver = self.driver
        self.create_Meetup(self.driver,1, cancel=True)
        cancel = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.ID,'MeetUpcancel')))
        cancel.click()
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID,'linkOfMeetUpHeading')))
        self.assertEqual(driver.current_url, 'http://127.0.0.1:5981/apps/_design/bell/MyApp/index.html#meetups')

    if __name__ == "__main__":
        unittest.main()