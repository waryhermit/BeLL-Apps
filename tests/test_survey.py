"""This module is used to test the survey funtionality of the BeLL app. """
import unittest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

import bell
from base_case import BaseCase, browsers, on_platforms


@on_platforms(browsers)
class SurveyTest(BaseCase):
    """Contains the unit tests and helper functions required to test
     the survey features of the BeLL app."""

    def setUp(self):
        self.accept_next_alert = True
        BaseCase.setUp(self)
        print("setup ran")

    def test_add_surveys(self):
        """Adds two surveys"""

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
        """Tests the process of deleting a survey."""
        driver = self.driver
        bell.login(driver, "admin", "password")
        self.go_to_surveys()
        self.add_survey()
        self.driver.back()
        self.driver.back()
        self.driver.refresh()
        self.assertTrue(self.delete_survey())

    def go_to_surveys(self):
        """Navigates to the survey page"""
        driver = self.driver
        wait = WebDriverWait(driver, 15)
        driver.find_element_by_id("NationManagerLink").click()
        btn_xpath = '//*[@id="surveys"]/tbody/tr[1]/th/a'
        wait.until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
        survey_btn = driver.find_element_by_xpath(btn_xpath)
        old_page = survey_btn
        survey_btn.click()

        # Clicking on the surveys link doesn't always work,
        # so keep trying until we are at the meetups page.
        # This might only be needed due to a bug in the site see:
        # https://github.com/open-learning-exchange/BeLL-Apps/issues/585
        wait = WebDriverWait(driver, 5)
        keeptrying = True
        numoftries = 0
        survay_xpath = '//*[@id="surveys"]/tbody/tr[1]/th/a'
        while keeptrying:
            try:
                # If the old page is stale then we are on the meetups tab.
                wait.until(EC.staleness_of(old_page))
                keeptrying = False
            except TimeoutException:
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, survay_xpath)))
                survey_btn = driver.find_element_by_xpath(survay_xpath)
                survey_btn.click()
                numoftries = numoftries + 1
                if numoftries == 6:
                    # If we still haven't got there something else went wrong.
                    keeptrying = False
                    return False

    def delete_survey(self):
        """Deletes a survey"""
        driver = self.driver
        wait = WebDriverWait(driver, 30)
        delete_xpath = '//*[@id="parentDiv"]/table/tbody/tr[2]/td[7]/a[3]'
        wait.until(EC.element_to_be_clickable((By.XPATH, delete_xpath)))
        delete_btn = driver.find_element_by_xpath(delete_xpath)
        delete_btn.click()
        expected = "Are you sure you want to delete this survey?"
        result = self.close_alert_and_get_its_text()
        return expected == result

    def add_survey(self):
        """Adds a survey."""
        driver = self.driver
        # TODO: Check url
        wait = WebDriverWait(driver, 30)
        add_xpath = "//a[contains(@href, '#survey/add')]"
        wait.until(EC.element_to_be_clickable((By.XPATH, add_xpath)))
        survey_add_btn = driver.find_element_by_xpath(add_xpath)
        survey_add_btn.click()

        wait.until(EC.element_to_be_clickable((By.NAME, "SurveyTitle")))
        survey_name = driver.find_element_by_name("SurveyTitle")
        survey_name.clear()
        survey_name.send_keys("Test Survey")
        wait.until(EC.element_to_be_clickable((By.NAME, "save")))
        save_btn = driver.find_element_by_name("save")
        save_btn.click()
        wait.until(EC.alert_is_present())
        expected = "Survey Saved!"
        result = self.close_alert_and_get_its_text()
        return result == expected

    def add_survey_question(self):
        """Adds a survey. Does not fill it our or save it."""
        driver = self.driver
        short_wait = WebDriverWait(driver, 5)
        long_wait = WebDriverWait(driver, 30)
        # driver.find_element_by_id("addQuestion").click()
        long_wait.until(EC.element_to_be_clickable((By.ID, "addQuestion")))
        add_question = driver.find_element_by_id("addQuestion")
        add_question.click()
        # Clicking on the surveys link doesn't always work,
        # so keep trying until we are at the meetups page.
        # This might only be needed due to a bug in the site see:
        # https://github.com/open-learning-exchange/BeLL-Apps/issues/585
        keeptrying = True
        numoftries = 0

        while keeptrying:
            try:
                # If the old page is stale then we are on the meetups tab.
                short_wait.until(EC.staleness_of(add_question))
                keeptrying = False
            except TimeoutException:
                long_wait.until(EC.element_to_be_clickable(
                    (By.ID, "add_new_question")))
                add_new_question = driver.find_element_by_id(
                    "add_new_question")
                add_new_question.click()
                numoftries = numoftries + 1
                if numoftries == 6:
                    # If we still haven't got there something else went wrong.
                    keeptrying = False
                    return False

    def multiple_choice_question(self):
        """"Fills out the information for a multiple choice question."""
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
        """"Fills out the information for a rating question."""
        driver = self.driver
        wait = WebDriverWait(driver, 30)
        wait.until(EC.element_to_be_clickable((By.ID, "add_new_question")))
        add_q_type = driver.find_element_by_id("add_new_question")
        Select(add_q_type).select_by_visible_text("Rating Scale")
        q_txt_xpath = "(//textarea[@id='question_text'])[4]"
        q_text = driver.find_element_by_xpath(q_txt_xpath)
        q_text.clear()
        q_text.send_keys("This is another test question.")

        select_rating = driver.find_element_by_id("select_rating")
        Select(select_rating).select_by_visible_text("5 ratings")

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
        """"Fills out the information for a single line text question."""

        driver = self.driver
        add_new_q = driver.find_element_by_id("add_new_question")
        Select(add_new_q).select_by_visible_text("Single Textbox")
        text_xpath = "(//textarea[@id='question_text'])[2]"
        q_text = driver.find_element_by_xpath(text_xpath)
        q_text.clear()
        q_text.send_keys("You must enter some text for this question.")
        req_xpath = "(//input[@id='required_question'])[2]"
        is_required = driver.find_element_by_xpath(req_xpath)
        is_required.click()
        self.save_question()

    def multiline_text_question(self):
        """"Fills out the information for a paragraph text question."""
        driver = self.driver
        question_type = driver.find_element_by_id("add_new_question")
        select_question_type = Select(question_type)
        select_question_type.select_by_visible_text("Comment/Essay Box")
        q_txt_xpath = "(//textarea[@id='question_text'])[3]"
        q_txt = driver.find_element_by_xpath(q_txt_xpath)
        q_txt.clear()
        q_txt.send_keys("This is an optional question.")
        self.save_question()

    def rearrange_questions(self):
        """Moves the questions around. Not finished."""
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
        """Saves the currently open question."""
        driver = self.driver
        wait = WebDriverWait(driver, 30)
        x_path = '//*[@id="1"]/div/input'
        wait.until(EC.presence_of_element_located((By.XPATH, x_path)))
        save_btn = driver.find_element_by_xpath(x_path)
        scroll_script = "return arguments[0].scrollIntoView();"
        driver.execute_script(scroll_script, save_btn)
        save_btn.click()
        expected = "Question has been saved"
        result = self.close_alert_and_get_its_text()
        self.assertEqual(expected, result)

    def choose_users_by_criteria(self):
        """Not Finished."""
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
        """Selects all users in the first BeLL."""
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
        """"Closes the currently open alert and returns its text."""
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
