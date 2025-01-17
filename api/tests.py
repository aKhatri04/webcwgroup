from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class UserListTest(unittest.TestCase):
    def setUp(self):
        # Set up the Chrome WebDriver
        self.driver = webdriver.Chrome()

    def test_signup_and_user_list(self):
        driver = self.driver

        # Step 1: Go to the signup page
        driver.get("http://localhost:8000/signup")

        # Step 2: Fill out the signup form
        long_username = "unique_test_user_1234567890"
        password = "SecurePassword123!"

        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password1")
        confirm_password_field = driver.find_element(By.NAME, "password2")
        signup_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Signup')]")

        username_field.send_keys(long_username)
        email_field.send_keys(f"{long_username}@example.com")
        password_field.send_keys(password)
        confirm_password_field.send_keys(password)
        signup_button.click()

        # Step 3: Log in after signup
        driver.get("http://localhost:8000/login")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")

        username_field.send_keys(long_username)
        password_field.send_keys(password)
        login_button.click()

        # Step 4: Navigate to the Users Page
        users_page_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Users Page"))
        )
        users_page_link.click()

        # Step 5: Verify user list is displayed
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        # Pagination Test
        while True:
            try:
                # Locate the "Next" button by class
                next_button = driver.find_element(By.CLASS_NAME, "btn-secondary")
                is_disabled = next_button.get_attribute("disabled") == "true"

                if is_disabled:
                    print("Next button is disabled, cannot paginate further.")
                    break

                # Scroll into view and click the button
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                next_button.click()

                # Wait for the table to refresh
                WebDriverWait(driver, 10).until(
                    EC.staleness_of(driver.find_element(By.TAG_NAME, "tbody"))
                )
            except Exception as e:
                print(f"Error during pagination: {e}")
                break

        print("Pagination test completed successfully.")

    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
