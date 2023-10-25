import time
import pytest
import allure
from selenium import webdriver
from page import Page
from utils import get_current_day, fibonacci


@pytest.fixture(scope="session")
def driver(request):
    remote_url = "http://localhost:4444/wd/hub"
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(remote_url, options=options)

    def fin():
        driver.quit()

    request.addfinalizer(fin)
    return driver


def test_bank_operations(driver):
    with allure.step("Open page and perform operations"):
        page = Page(driver)

        page.open_page("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")
        page.click_customer_login_button()
        page.select_user_from_dropdown("Harry Potter")
        page.click_login_button_after_selection()
        page.click_deposit_button()
        fibonacci_value = fibonacci(get_current_day() + 1)
        page.fill_amount_field(fibonacci_value)
        page.click_submit_button("Deposit")
        page.click_withdraw_button()
        time.sleep(1)
        page.fill_amount_field(fibonacci_value)
        page.click_submit_button("Withdraw")
        balance = page.get_balance()
        assert balance == 0
        time.sleep(1)
        page.click_transactions_button()
        page.check_transactions_and_write_csv(fibonacci_value)
        with open('output.csv', 'rb') as file:
            allure.attach(file.read(), 'output.csv', allure.attachment_type.CSV)
