from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from .models import FriendRequest

User = get_user_model()

class TestSignup(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome() 
        self.signup_url = f"{self.live_server_url}/signup/"

    def tearDown(self):
        self.driver.quit()

    def test_user_signup(self):
        self.driver.get(self.signup_url)
        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "password1").send_keys("password123")
        self.driver.find_element(By.NAME, "password2").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type=submit]").click()
        self.assertTrue(User.objects.filter(username="testuser").exists())

class TestLogin(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_url = f"{self.live_server_url}/login/"
        self.user = User.objects.create_user(username="testuser", password="password123")

    def tearDown(self):
        self.driver.quit()

    def test_user_login(self):
        self.driver.get(self.login_url)
        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type=submit]").click()
        self.assertIn("Main Page", self.driver.page_source)


class TestEditProfile(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.profile_url = f"{self.live_server_url}/profile/"
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.user.name = "Test User"
        self.user.email = "testuser@example.com"
        self.user.save()

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.get(f"{self.live_server_url}/login/")
        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type=submit]").click()

    def test_edit_profile(self):
        self.login()
        self.driver.get(self.profile_url)
        self.driver.find_element(By.CSS_SELECTOR, "button.edit-profile").click()
        name_input = self.driver.find_element(By.NAME, "name")
        name_input.clear()
        name_input.send_keys("Updated Name")
        self.driver.find_element(By.CSS_SELECTOR, "button.save-profile").click()
        # Reload user data
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Updated Name")

class TestFriendRequest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.send_request_url = f"{self.live_server_url}/request/"
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

    def tearDown(self):
        self.driver.quit()

    def login(self, username):
        self.driver.get(f"{self.live_server_url}/login/")
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type=submit]").click()

    def test_send_friend_request(self):
        self.login("user1")
        self.driver.get(self.send_request_url)
        self.driver.find_element(By.NAME, "to_username").send_keys("user2")
        self.driver.find_element(By.CSS_SELECTOR, "button.send-request").click()
        self.assertTrue(FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())