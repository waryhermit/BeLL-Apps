import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import bell
from base_case import BaseCase, browsers, on_platforms


@on_platforms(browsers)
class LoginTestCouchDB(BaseCase):
	""" Creates a member, then logins, logouts, and finally deletes the member from CouchDB. """
	#TODO : Test if logged in
	#TODO : Test if logged out
	#TODO : Test if deleted
	def test_login_bycouchdb(self):
		bell.create_member()
		driver = self.driver
        
        # login
		bell.login_test(self.driver, "q", "q")
        
        # wait for the next page
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard")))
		self.logout_test()
		bell.delete_member()
		
	def logout_test(self):
		""" NoneType -> NoneType
		Helper function testing a correct logout operation.
		"""
		driver = self.driver
		# test logout
		bell.logout(driver)
		# ensure logout was successful
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login")))
		actual = driver.current_url
		expected = "http://127.0.0.1:5981/apps/_design/bell/MyApp/index.html#login"
		self.assertEqual(actual, expected)	
		
if __name__ == "__main__":
    unittest.main()
