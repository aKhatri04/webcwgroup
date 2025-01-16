from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class SignupPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://127.0.0.1:8000/signup")  # Replace with your actual signup page URL

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_signup_page_loads(self):
        """Test that the signup page loads correctly."""
        self.assertIn("Signup", self.driver.title)
        header = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(header, "Signup")

    def test_signup_form_submission_valid(self):
        """Test successful signup form submission."""
        driver = self.driver

        # Fill out the signup form
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
        driver.find_element(By.NAME, "password1").send_keys("Testpassword123!")
        driver.find_element(By.NAME, "password2").send_keys("Testpassword123!")

        # Submit the form
        driver.find_element(By.XPATH, "//button[text()='Signup']").click()

        # Wait for the redirect to the login page
        WebDriverWait(driver, 10).until(EC.url_contains("/login"))
        
        # Check if redirected to login page
        self.assertIn("login", driver.current_url)

    def test_signup_form_submission_invalid(self):
        """Test form submission with invalid data."""
        driver = self.driver

        # Clear and fill out the form with mismatched passwords
        driver.find_element(By.NAME, "username").send_keys("testuser2")
        driver.find_element(By.NAME, "email").send_keys("testuser2@example.com")
        driver.find_element(By.NAME, "password1").send_keys("Testpassword123!")
        driver.find_element(By.NAME, "password2").send_keys("DifferentPassword123!")

        # Submit the form
        driver.find_element(By.XPATH, "//button[text()='Signup']").click()

        # Wait for error message to appear
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".errorlist"))
        )

        self.assertTrue(error_message.is_displayed())
        self.assertIn("The two password fields didn't match.", error_message.text)

if __name__ == "__main__":
    unittest.main()


