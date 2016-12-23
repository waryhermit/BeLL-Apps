import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

import bell
from base_case import BaseCase, browsers, on_platforms


@on_platforms(browsers)
class SurveyTest(BaseCase):

    def setUp(self):
        self.accept_next_alert = True
        BaseCase.setUp(self)
        print("setup ran")

    def test_add_surveys(self):

        driver = self.driver
        bell.login(driver, "admin", "password")
        self.go_to_surveys()
        self.add_survey()
        self.add_survey_question()
        self.multiple_choice_question()
        self.add_survey_question()
        self.rating_question()
        self.add_survey_question()
        self.single_text_question()
        self.add_survey_question()
        self.multiline_text_question()
        self.choose_users()

    def test_delete_survey(self):
        driver = self.driver
        bell.login(driver, "admin", "password")
        self.go_to_surveys()
        self.add_survey()
        self.driver.back()
        self.driver.back()
        self.driver.refresh()
        self.assertTrue(self.delete_survey())

    def go_to_surveys(self):
        driver = self.driver
        wait = WebDriverWait(driver, 5)
        driver.find_element_by_id("NationManagerLink").click()

        survey_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="surveys"]/tbody/tr[1]/th/a')))
        old_page = survey_btn
        survey_btn.click()

        # Clicking on the surveys link doesn't always work, so keep trying until we are at the meetups page.
        # This might only be needed due to a bug in the site see:
        # https://github.com/open-learning-exchange/BeLL-Apps/issues/585
        keeptrying = True
        numoftries = 0
        while (keeptrying):
            try:
                # If the old page is stale then we are on the meetups tab.
                wait.until(EC.staleness_of(old_page))
                keeptrying = False
            except TimeoutException:
                survey_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="surveys"]/tbody/tr[1]/th/a')))
                survey_btn.click()
                numoftrys = numoftries + 1
                if (numoftries == 6):
                    # If we still haven't got there something else went wrong.
                    keeptrying = False
                    return False

    def delete_survey(self):
        driver = self.driver
        delete_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="parentDiv"]/table/tbody/tr[2]/td[7]/a[3]')))
        delete_btn.click()
        return ("Are you sure you want to delete this survey?" == self.close_alert_and_get_its_text())

    def add_survey(self):
        driver = self.driver
        # TODO: Check url
        driver = self.driver
        survey_add_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#survey/add')]")))
        survey_add_btn.click()
        survey_name = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.NAME, "SurveyTitle")))
        survey_name.clear()
        survey_name.send_keys("Test Survey")
        save_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.NAME, "save")))
        save_btn.click()
        WebDriverWait(driver, 30).until(EC.alert_is_present())
        return ("Survey Saved!" == self.close_alert_and_get_its_text())

    def add_survey_question(self):
        driver = self.driver
        wait = WebDriverWait(driver, 5)

        # driver.find_element_by_id("addQuestion").click()
        addQuestion = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "addQuestion"))).click()
        # Clicking on the surveys link doesn't always work, so keep trying until we are at the meetups page.
        # This might only be needed due to a bug in the site see:
        # https://github.com/open-learning-exchange/BeLL-Apps/issues/585
        keeptrying = True
        numoftries = 0
        while (keeptrying):
            try:
                # If the old page is stale then we are on the meetups tab.
                wait.until(EC.staleness_of(addQuestion))
                keeptrying = False
            except TimeoutException:
                add_new_question = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, "add_new_question")))
                add_new_question.click()
                numoftrys = numoftries + 1
                if (numoftries == 6):
                    # If we still haven't got there something else went wrong.
                    keeptrying = False
                    return False

    def multiple_choice_question(self):
        driver = self.driver
        driver.find_element_by_id("question_text").clear()
        driver.find_element_by_id("question_text").send_keys(
            "This is a test Question.")
        driver.find_element_by_id("answer_choices").clear()
        driver.find_element_by_id("answer_choices").send_keys(
            "Choice 1\nChoice 2\nChoice 3")
        driver.find_element_by_id("required_question").click()
        self.save_question()

    def rating_question(self):
        driver = self.driver
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "add_new_question")))
        Select(driver.find_element_by_id("add_new_question")
               ).select_by_visible_text("Rating Scale")
        driver.find_element_by_xpath(
            "(//textarea[@id='question_text'])[4]").clear()
        driver.find_element_by_xpath(
            "(//textarea[@id='question_text'])[4]").send_keys("This is another test question.")
        Select(driver.find_element_by_id("select_rating")
               ).select_by_visible_text("5 ratings")

        rating1_label = driver.find_element_by_name("rating1_label")
        driver.execute_script(
            "return arguments[0].scrollIntoView();", rating1_label)
        rating1_label("rating1_label").clear()
        rating1_label.send_keys("Rating 1")

        rating2_label = driver.find_element_by_name("rating2_label")
        driver.execute_script(
            "return arguments[0].scrollIntoView();", rating2_label)
        rating2_label.clear()
        rating2_label.send_keys("Rating 2")

        rating3_label = driver.find_element_by_name("rating3_label")
        driver.execute_script(
            "return arguments[0].scrollIntoView();", rating3_label)
        rating2_label.clear()
        rating2_label.send_keys("Rating 3")

        rating4_label = driver.find_element_by_name("rating4_label")
        driver.execute_script(
            "return arguments[0].scrollIntoView();", rating4_label)
        rating2_label.clear()
        rating2_label.send_keys("Rating 4")

        rating5_label = driver.find_element_by_name("rating5_label")
        driver.execute_script(
            "return arguments[0].scrollIntoView();", rating5_label)
        rating2_label.clear()
        rating2_label.send_keys("Rating 5")

        required_question = driver.find_element_by_xpath(
            "(//input[@id='required_question'])[4]")
        driver.execute_script(
            "return arguments[0].scrollIntoView();", required_question)
        required_question.click()

        save_btn = driver.find_element_by_xpath(
            "(//input[@value='Save Question'])[4]")
        driver.execute_script(
            "return arguments[0].scrollIntoView();", save_btn)
        save_btn.click()
        self.assertEqual("Please provide atleast one options",
                         self.close_alert_and_get_its_text())
        answer_choices = driver.find_element_by_xpath(
            "(//textarea[@id='answer_choices'])[2]")
        driver.execute_script(
            "return arguments[0].scrollIntoView();", answer_choices)

        answer_choices.clear()
        answer_choices.send_keys(
            "Option 1\nOption 2\nOption 3\nOption 4\nOption 5")
        self.save_question()

    def single_text_question(self):
        driver = self.driver
        Select(driver.find_element_by_id("add_new_question")
               ).select_by_visible_text("Single Textbox")
        driver.find_element_by_xpath(
            "(//textarea[@id='question_text'])[2]").clear()
        driver.find_element_by_xpath("(//textarea[@id='question_text'])[2]").send_keys(
            "You must enter some text for this question.")
        driver.find_element_by_xpath(
            "(//input[@id='required_question'])[2]").click()
        self.save_question()

    def multiline_text_question(self):
        driver = self.driver
        Select(driver.find_element_by_id("add_new_question")
               ).select_by_visible_text("Comment/Essay Box")
        driver.find_element_by_xpath(
            "(//textarea[@id='question_text'])[3]").clear()
        driver.find_element_by_xpath(
            "(//textarea[@id='question_text'])[3]").send_keys("This is an optional question.")
        self.save_question()

    def rearrange_questions(self):
        driver = self.driver
        driver.find_element_by_id("Rearrange").click()
        driver.find_element_by_id("movedown").click()
        driver.find_element_by_name("questionRow").click()
        driver.find_element_by_id("movedown").click()
        driver.find_element_by_xpath(
            "(//input[@name='questionRow'])[3]").click()
        driver.find_element_by_id("moveup").click()
        driver.find_element_by_id("Rearrange").click()

    def save_question(self):
        driver = self.driver
        save_btn = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="1"]/div/input')))
        driver.execute_script(
            "return arguments[0].scrollIntoView();", save_btn)
        save_btn.click()

        self.assertEqual("Question has been saved",
                         self.close_alert_and_get_its_text())

    def choose_users_by_criteria(self):
        driver = self.driver
        driver.find_element_by_css_selector("button.btn.btn-info").click()
        driver.find_element_by_name("genderSelector").click()
        driver.find_element_by_xpath(
            "(//input[@name='genderSelector'])[2]").click()
        driver.find_element_by_name("ageGroupSelector").click()
        driver.find_element_by_xpath(
            "(//input[@name='ageGroupSelector'])[2]").click()
        driver.find_element_by_xpath(
            "(//input[@name='ageGroupSelector'])[3]").click()
        driver.find_element_by_xpath(
            "(//input[@name='ageGroupSelector'])[4]").click()
        driver.find_element_by_xpath(
            "(//input[@name='ageGroupSelector'])[5]").click()
        driver.find_element_by_name("rolesSelector").click()
        driver.find_element_by_xpath(
            "(//input[@name='rolesSelector'])[2]").click()
        driver.find_element_by_xpath(
            "(//input[@name='rolesSelector'])[3]").click()
        driver.find_element_by_name("bellSelector").click()
        driver.find_element_by_name("includeAdmins").click()
        driver.find_element_by_id("UnSelectAllCriteria").click()
        driver.find_element_by_id("selectAllCriteria").click()

        driver.find_element_by_id("formButton").click()
        self.assertEqual("No members have been found for the selected options",
                         self.close_alert_and_get_its_text())
        driver.find_element_by_id("returnBack").click()

    def choose_users(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "//div[@id='main-body']/div/button[3]").click()
        driver.find_element_by_name("bellSelector").click()
        driver.find_element_by_id("openMembersList").click()
        driver.find_element_by_name("surveyMember").click()
        driver.find_element_by_name("includeAdmins").click()
        driver.find_element_by_id("UnSelectAllMembers").click()
        driver.find_element_by_id("selectAllMembers").click()
        driver.find_element_by_id("sendSurveyToSelectedList").click()
        self.assertEqual("Survey has been sent successfully",
                         self.close_alert_and_get_its_text())

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True
if __name__ == '__main__':
    unittest.main()
