from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import unittest

class SignupTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:8000/signup")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_signup_form_submission_valid(self):
        """Test successful signup with valid data."""
        driver = self.driver

        # Clear input fields and enter valid data
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("amartest1234")
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys("amartest123@example.com")
        driver.find_element(By.NAME, "password1").clear()
        driver.find_element(By.NAME, "password1").send_keys("Testpassword123!")
        driver.find_element(By.NAME, "password2").clear()
        driver.find_element(By.NAME, "password2").send_keys("Testpassword123!")

        # Click the signup button
        driver.find_element(By.XPATH, "//button[text()='Signup']").click()

        # Print the page source for debugging (optional)
        print(driver.page_source)

        # Wait for redirection to login page and verify
        WebDriverWait(driver, 20).until(EC.url_contains("/login"))
        self.assertIn("login", driver.current_url)

    def test_signup_form_submission_invalid(self):
        """Test signup with mismatched passwords."""
        driver = self.driver

        # Clear input fields and enter mismatched passwords
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("amartest456")
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys("amartest456@example.com")
        driver.find_element(By.NAME, "password1").clear()
        driver.find_element(By.NAME, "password1").send_keys("Testpassword123!")
        driver.find_element(By.NAME, "password2").clear()
        driver.find_element(By.NAME, "password2").send_keys("DifferentPassword123!")

        # Click the signup button
        driver.find_element(By.XPATH, "//button[text()='Signup']").click()

        # Wait for the error message to appear and verify its contents
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".errorlist"))
        )

        self.assertTrue(error_message.is_displayed())
        self.assertIn("The two password fields didn’t match.", error_message.text)



class EditUserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:8000/login")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_edit_user_info(self):
        driver = self.driver

        print("Attempting to log in...")
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("amartest123")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("Testpassword123!")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        print("Waiting for redirection to the main page...")
        WebDriverWait(driver, 30).until(EC.url_contains("/"))
        print("Redirection successful, current URL:", driver.current_url)

        print("Navigating to the profile page...")
        profile_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Profile Page"))
        )
        profile_link.click()
        WebDriverWait(driver, 30).until(EC.url_contains("/profile"))
        print("Profile page loaded, current URL:", driver.current_url)

        print("Clicking the edit button...")
        edit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Edit']"))
        )
        edit_button.click()

        print("Updating user information...")
        name_field = driver.find_element(By.XPATH, "//input[@placeholder='Name']")
        name_field.clear()
        name_field.send_keys("Updated Name")

        email_field = driver.find_element(By.XPATH, "//input[@placeholder='Email']")
        email_field.clear()
        email_field.send_keys("updatedemail@example.com")

        dob_field = driver.find_element(By.XPATH, "//input[@type='date']")
        dob_field.clear()
        dob_field.send_keys("01-01-2000")

        print("Adding a new hobby...")
        new_hobby_field = driver.find_element(By.XPATH, "//input[@placeholder='New Hobby']")
        new_hobby_field.send_keys("New Hobby")
        create_hobby_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Create Hobby']"))
        )
        create_hobby_button.click()

        print("Saving the updated profile...")
        save_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']"))
        )
        save_button.click()

        print("Verifying updates...")
        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element((By.XPATH, "//p[contains(text(), 'Name: Updated Name')]"), "Updated Name")
        )
        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element((By.XPATH, "//p[contains(text(), 'Email: updatedemail@example.com')]"),
                                             "updatedemail@example.com")
        )
        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element((By.XPATH, "//p[contains(text(), 'Date of Birth: 2000-01-01')]"),
                                             "2000-01-01")
        )
        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element((By.XPATH, "//p[contains(text(), 'Hobbies')]"), "New Hobby")
        )
        print("All updates verified successfully.")



class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:8000/signup")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_signup_and_login(self):
        """Test signing up and logging in with the same credentials."""
        driver = self.driver

        # Sign up a new user
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("amartest321")
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys("amartest321@example.com")
        driver.find_element(By.NAME, "password1").clear()
        driver.find_element(By.NAME, "password1").send_keys("Testpassword123!")
        driver.find_element(By.NAME, "password2").clear()
        driver.find_element(By.NAME, "password2").send_keys("Testpassword123!")

        # Submit the signup form
        driver.find_element(By.XPATH, "//button[text()='Signup']").click()

        # Wait for redirection to the login page and verify the URL
        WebDriverWait(driver, 20).until(EC.url_contains("/login"))
        self.assertIn("login", driver.current_url)

        # Log in with the same credentials
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("amartest321")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("Testpassword123!")

        # Submit the login form
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        # Wait for redirection to the homepage and verify the URL
        WebDriverWait(driver, 20).until(EC.url_contains("/"))

        # Ensure the user is no longer on the login page
        self.assertNotIn("login", driver.current_url)

class FriendRequestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:8000/login")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_send_friend_request(self):
        driver = self.driver

        # Log in as an existing user
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("amartest321")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("Testpassword123!")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        # Wait for the redirection to the home page and verify successful login
        WebDriverWait(driver, 20).until(EC.url_contains("/"))
        self.assertNotIn("login", driver.current_url)

        # Navigate to the "Send Request" page
        driver.find_element(By.LINK_TEXT, "Send Request Page").click()
        WebDriverWait(driver, 20).until(EC.url_contains("/request"))

        # Enter a username and send a friend request
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter username']"))
        )
        username_input.clear()
        username_input.send_keys("amartest1234")

        driver.find_element(By.XPATH, "//button[text()='Send Request']").click()

        # Handle confirmation or error message
        try:
            # Wait for the alert to appear and verify its text
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert_text = alert.text
            print("Alert appeared with text:", alert_text)

            self.assertIn("Friend request sent!", alert_text)

            # Accept the alert
            alert.accept()
            print("Alert accepted.")

        except TimeoutException:
            try:
                # Wait for an error message if no alert is displayed
                error_message_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".text-danger"))
                )
                error_message = error_message_element.text
                self.assertTrue(error_message_element.is_displayed())
                print("Error:", error_message)
            except TimeoutException:
                # Fail the test if neither alert nor error message appears
                self.fail("No confirmation alert or error message displayed.")

class AcceptFriendRequestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:8000/login")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_accept_friend_request(self):
        driver = self.driver

        # Log in as a user
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("amartest123")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("Testpassword123!")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        # Wait for redirection to the home page and verify successful login
        WebDriverWait(driver, 20).until(EC.url_contains("/"))
        self.assertNotIn("login", driver.current_url)

        # Navigate to the "Pending Requests" page
        driver.find_element(By.LINK_TEXT, "Pending Requests Page").click()
        WebDriverWait(driver, 20).until(EC.url_contains("/pending"))

        # Verify pending friend requests exist
        try:
            pending_requests = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul/li"))
            )
            self.assertGreater(len(pending_requests), 0, "No pending friend requests found.")
        except TimeoutException:
            self.fail("No pending friend requests displayed.")

        # Attempt to accept a friend request
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept']"))
            )
            accept_button.click()

            # Wait for the alert to appear and verify its text
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert_text = alert.text
            print("Alert appeared with text:", alert_text)

            # Assert the alert text
            self.assertIn("Friend request accepted!", alert_text)

            # Accept the alert
            alert.accept()
            print("Friend request accepted and alert handled.")
        except TimeoutException:
            self.fail("Failed to accept friend request or alert did not appear.")


class RejectFriendRequestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:8000/login")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_reject_friend_request(self):
        driver = self.driver

        # Log in as a user
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("amartest1234")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("Testpassword123!")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        # Wait for redirection to the home page and verify successful login
        WebDriverWait(driver, 20).until(EC.url_contains("/"))
        self.assertNotIn("login", driver.current_url)

        # Navigate to the "Pending Requests" page
        driver.find_element(By.LINK_TEXT, "Pending Requests Page").click()
        WebDriverWait(driver, 20).until(EC.url_contains("/pending"))

        # Verify pending friend requests exist
        try:
            pending_requests = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul/li"))
            )
            self.assertGreater(len(pending_requests), 0, "No pending friend requests found.")
        except TimeoutException:
            self.fail("No pending friend requests displayed.")

        # Attempt to reject a friend request
        try:
            reject_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Reject']"))
            )
            reject_button.click()

            # Wait for the alert to appear and verify its text
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert_text = alert.text
            print("Alert appeared with text:", alert_text)

            # Assert the alert text
            self.assertIn("Friend request rejected!", alert_text)

            # Accept the alert
            alert.accept()
            print("Friend request rejected and alert handled.")
        except TimeoutException:
            self.fail("Failed to reject friend request or alert did not appear.")

class UserListTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:8000/login")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_view_user_list_and_pagination(self):
        driver = self.driver

        # Log in as a user
        print("Attempting to log in...")
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("amartest123")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("Testpassword123!")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        # Wait for redirection to the main page and verify successful login
        WebDriverWait(driver, 20).until(EC.url_contains("/"))
        print("Logged in successfully.")

        # Navigate to the "Users Page"
        print("Navigating to the Users Page...")
        driver.find_element(By.LINK_TEXT, "Users Page").click()
        WebDriverWait(driver, 20).until(EC.url_contains("/users"))
        print("Users Page loaded.")

        # Verify the user list table is displayed
        try:
            user_table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table"))
            )
            self.assertTrue(user_table.is_displayed(), "User list table is not displayed.")
        except TimeoutException:
            self.fail("User list table did not load.")

        # Test pagination with page number buttons before filtering
        print("Testing pagination with page numbers (before filtering)...")
        try:
            # Navigate to page 2
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='2']"))
            )
            page_2_button = driver.find_element(By.XPATH, "//button[text()='2']")
            page_2_button.click()

            # Wait for the page to update and re-locate the active button
            WebDriverWait(driver, 10).until(
                lambda d: "btn-primary active" in driver.find_element(By.XPATH, "//button[text()='2']").get_attribute(
                    "class"
                )
            )
            print("Navigated to page 2 successfully.")

            # Verify users on page 2
            rows_page_2 = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
            self.assertGreater(len(rows_page_2), 0, "No users displayed on page 2.")
            print(f"Number of users on page 2: {len(rows_page_2)}")

            # Navigate back to page 1
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='1']"))
            )
            page_1_button = driver.find_element(By.XPATH, "//button[text()='1']")
            page_1_button.click()

            # Wait for the page to update and re-locate the active button
            WebDriverWait(driver, 10).until(
                lambda d: "btn-primary active" in driver.find_element(By.XPATH, "//button[text()='1']").get_attribute(
                    "class"
                )
            )
            print("Navigated back to page 1 successfully.")

            # Verify users on page 1
            rows_page_1 = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
            self.assertGreater(len(rows_page_1), 0, "No users displayed on page 1.")
            print(f"Number of users on page 1: {len(rows_page_1)}")

        except TimeoutException:
            self.fail("Pagination with page numbers did not work as expected.")

        # Test filtering by age range
        print("Testing filters...")
        min_age_input = driver.find_element(By.ID, "minAge")
        max_age_input = driver.find_element(By.ID, "maxAge")

        min_age_input.clear()
        min_age_input.send_keys("20")
        max_age_input.clear()
        max_age_input.send_keys("30")
        driver.find_element(By.XPATH, "//button[text()='Apply Filters']").click()

        # Wait for the filtered results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )
        print("Filters applied successfully.")

        # Verify that the user list changes after applying the filter
        rows_after_filter = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        self.assertGreater(len(rows_after_filter), 0, "No users displayed after applying filters.")
        print(f"Number of users displayed after filtering: {len(rows_after_filter)}")

        print("User list and pagination test completed successfully.")





if __name__ == "__main__":
    unittest.main()