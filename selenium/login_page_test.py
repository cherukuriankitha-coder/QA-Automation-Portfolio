"""Selenium Page Object Model example for a QA automation portfolio."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH = (By.ID, "flash")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("https://the-internet.herokuapp.com/login")

    def login(self, username: str, password: str):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME)).send_keys(username)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.SUBMIT).click()

    def flash_message(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.FLASH)).text


def test_valid_login():
    driver = webdriver.Chrome()
    try:
        page = LoginPage(driver)
        page.open()
        page.login("tomsmith", "SuperSecretPassword!")
        assert "You logged into a secure area!" in page.flash_message()
    finally:
        driver.quit()
