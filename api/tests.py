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
        cls.driver.get("http://127.0.0.1:8000/signup")  

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    

    def test_signup_form_submission_valid(self):
        """Test successful signup with valid data."""
        driver = self.driver

        
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("testuser1212")
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys("testuser1212@example.com")
        driver.find_element(By.NAME, "password1").clear()
        driver.find_element(By.NAME, "password1").send_keys("Testpassword123!")
        driver.find_element(By.NAME, "password2").clear()
        driver.find_element(By.NAME, "password2").send_keys("Testpassword123!")

       
        driver.find_element(By.XPATH, "//button[text()='Signup']").click()

        
        print(driver.page_source)

        
        WebDriverWait(driver, 20).until(EC.url_contains("/login"))

        
        self.assertIn("login", driver.current_url)

    def test_signup_form_submission_invalid(self):
        """Test signup with mismatched passwords."""
        driver = self.driver

        
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("testuser2")
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys("testuser2@example.com")
        driver.find_element(By.NAME, "password1").clear()
        driver.find_element(By.NAME, "password1").send_keys("Testpassword123!")
        driver.find_element(By.NAME, "password2").clear()
        driver.find_element(By.NAME, "password2").send_keys("DifferentPassword123!")

        
        driver.find_element(By.XPATH, "//button[text()='Signup']").click()

        
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".errorlist"))
        )

       
        self.assertTrue(error_message.is_displayed())
        self.assertIn("The two password fields didn’t match.", error_message.text)



class EditUserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://127.0.0.1:8000/login") 

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_edit_user_info(self):
        driver = self.driver

        
        print("Attempting to log in...")
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("testuser1234")
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
            EC.text_to_be_present_in_element((By.XPATH, "//p[contains(text(), 'Email: updatedemail@example.com')]"), "updatedemail@example.com")
        )
        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element((By.XPATH, "//p[contains(text(), 'Date of Birth: 2000-01-01')]"), "2000-01-01")
        )
        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element((By.XPATH, "//p[contains(text(), 'Hobbies')]"), "New Hobby")
        )
        print("All updates verified successfully.")



class LoginTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://127.0.0.1:8000/signup") 

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_signup_and_login(self):
        """Test signing up and logging in with the same credentials."""
        driver = self.driver

       
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("testuser1234")
        driver.find_element(By.NAME, "email").clear()
        driver.find_element(By.NAME, "email").send_keys("testuser1234@example.com")
        driver.find_element(By.NAME, "password1").clear()
        driver.find_element(By.NAME, "password1").send_keys("Testpassword123!")
        driver.find_element(By.NAME, "password2").clear()
        driver.find_element(By.NAME, "password2").send_keys("Testpassword123!")

        
        driver.find_element(By.XPATH, "//button[text()='Signup']").click()

       
        WebDriverWait(driver, 20).until(EC.url_contains("/login"))
        self.assertIn("login", driver.current_url)

       
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("testuser1234")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("Testpassword123!")

        
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        
        WebDriverWait(driver, 20).until(EC.url_contains("/"))

        
        self.assertNotIn("login", driver.current_url)

class FriendRequestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://127.0.0.1:8000/login")  

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_send_friend_request(self):
        driver = self.driver

        
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("newTestUser")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("Testpassword123!")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        
        WebDriverWait(driver, 20).until(EC.url_contains("/"))
        self.assertNotIn("login", driver.current_url)

        
        driver.find_element(By.LINK_TEXT, "Send Request Page").click()
        WebDriverWait(driver, 20).until(EC.url_contains("/request"))

        
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter username']"))
        )
        username_input.clear()
        username_input.send_keys("test10")  

        
        driver.find_element(By.XPATH, "//button[text()='Send Request']").click()
        
        try:
        
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert_text = alert.text
            print("Alert appeared with text:", alert_text)

    
            self.assertIn("Friend request sent!", alert_text)

    
            alert.accept()
            print("Alert accepted.")

        except TimeoutException:
            try:
        
                error_message_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".text-danger")))
                error_message = error_message_element.text
                self.assertTrue(error_message_element.is_displayed())
                print("Error:", error_message)
            except TimeoutException:
                self.fail("No confirmation alert or error message displayed.")

class AcceptFriendRequestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://127.0.0.1:8000/login")  

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_accept_friend_request(self):
        driver = self.driver

        
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("testUser12345")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("Testpassword123!")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        
        WebDriverWait(driver, 20).until(EC.url_contains("/"))
        self.assertNotIn("login", driver.current_url)

        
        driver.find_element(By.LINK_TEXT, "Pending Requests Page").click()
        WebDriverWait(driver, 20).until(EC.url_contains("/pending"))

        
        try:
            pending_requests = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul/li"))
            )
            self.assertGreater(len(pending_requests), 0, "No pending friend requests found.")
        except TimeoutException:
            self.fail("No pending friend requests displayed.")

        
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept']"))
            )
            accept_button.click()

            
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
        cls.driver.get("http://127.0.0.1:8000/login")  

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_accept_friend_request(self):
        driver = self.driver

        
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys("testUser12345")
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys("Testpassword123!")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        
        WebDriverWait(driver, 20).until(EC.url_contains("/"))
        self.assertNotIn("login", driver.current_url)

        
        driver.find_element(By.LINK_TEXT, "Pending Requests Page").click()
        WebDriverWait(driver, 20).until(EC.url_contains("/pending"))

        
        try:
            pending_requests = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul/li"))
            )
            self.assertGreater(len(pending_requests), 0, "No pending friend requests found.")
        except TimeoutException:
            self.fail("No pending friend requests displayed.")

        #reject
        try:
            reject_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Reject']"))
            )
            reject_button.click()

            
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert_text = alert.text
            print("Alert appeared with text:", alert_text)

            
            self.assertIn("Friend request rejected!", alert_text)

            
            alert.accept()
            print("Friend request accepted and alert handled.")
        except TimeoutException:
            self.fail("Failed to accept friend request or alert did not appear.")

if __name__ == "__main__":
    unittest.main()




