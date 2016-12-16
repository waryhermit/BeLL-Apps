import unittest
import datetime

from base_case import on_platforms
from base_case import browsers
from base_case import BaseCase

from selenium import webdriver


@on_platforms(browsers)
class MeetupTest(BaseCase):
    """description of class"""


    def test_start_new_meetup(self):
        """ comment"""
        driver = self.driver

        driver.get("http://127.0.0.1:5985/apps/_design/bell/MyApp/index.html#meetups")

        submit = driver.find_element_by_id("linkOfMeetUpHeading")
        submit.click()

        elem = driver.find_element_by_name("title")
        elem.sendkeys("Test Meetup")
        elem = driver.find_element_by_name("description")
        elem.sendkeys("This is a test meeting automatically created by test_meetup.py")
        elem = driver.find_element_by_name("startDate")
        elem.sendkeys(datetime.datetime.now.strftime('%Y/%m/%d'))
        elem = driver.find_element_by_name("endDate")
        i = datetime.datetime.now() + datetime.timedelta(days=1)
        elem.sendkeys(i.strftime('%Y/%m/%d'))
        elem = driver.find_element_by_name("recurring")

        fields = ["title", "description", "startDate", "endDate", "recurring", "startTime", "endTime", "category", "meetupLocation"]
    
        # fill out all fields
        for field in fields:
            elem = driver.find_element_by_name(field)
            elem.send_keys("ole")

    def test_cancel_meetup(self):
        """ comment"""

    def test_invite_member(self):
        """ comment"""
    def test_multiday_meetup(self):
        """ comment"""
    def test_singleday_meetup(self):
        """ comment"""
    def recurring_meetup(self):
        """ comment"""

