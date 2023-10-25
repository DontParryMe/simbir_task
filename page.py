from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from utils import format_date, is_date, write_csv


class Page:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, condition, timeout=10):
        return WebDriverWait(self.driver, timeout).until(condition)

    def open_page(self, url):
        self.driver.get(url)

    def click_customer_login_button(self, timeout=10):
        customer_login_button = self.wait_for_element(
            ec.element_to_be_clickable((By.XPATH, '//button[text()="Customer Login"]')),
            timeout,
        )
        customer_login_button.click()

    def select_user_from_dropdown(self, username, timeout=10):
        dropdown = self.wait_for_element(
            ec.element_to_be_clickable((By.ID, 'userSelect')),
            timeout,
        )
        select = Select(dropdown)
        select.select_by_visible_text(username)

    def click_login_button_after_selection(self, timeout=10):
        login_button = self.wait_for_element(
            ec.element_to_be_clickable((By.XPATH, '//button[text()="Login"]')),
            timeout,
        )
        login_button.click()

    def click_deposit_button(self, timeout=10):
        deposit_button = self.wait_for_element(
            ec.element_to_be_clickable((By.XPATH, '//*[@ng-class="btnClass2"]',)),
            timeout,
        )
        deposit_button.click()

    def fill_amount_field(self, text, timeout=10):
        amount_field = self.wait_for_element(
            ec.element_to_be_clickable((By.XPATH, '//input[@placeholder="amount"]')),
            timeout,
        )
        amount_field.clear()
        amount_field.send_keys(text)

    def click_submit_button(self, text, timeout=10):
        submit_button_locator = (By.XPATH, f'//button[text()="{text}"]')
        submit_button = self.wait_for_element(
            ec.element_to_be_clickable(submit_button_locator),
            timeout,
        )
        submit_button.click()

    def click_withdraw_button(self, timeout=10):
        withdraw_button = self.wait_for_element(
            ec.element_to_be_clickable((By.XPATH, '//*[@ng-class="btnClass3"]',)),
            timeout,
        )
        withdraw_button.click()

    def click_transactions_button(self, timeout=10):
        transactions_button = self.wait_for_element(
            ec.element_to_be_clickable((By.XPATH, '//*[@ng-class="btnClass1"]')),
            timeout,
        )
        transactions_button.click()

    def get_transactions(self, timeout=10):
        table = self.wait_for_element(
            ec.presence_of_element_located((By.TAG_NAME, "table")),
            timeout,
        )
        rows = table.find_elements(By.TAG_NAME, "tr")
        transactions = []
        for row in rows:
            row_data = []
            cells = row.find_elements(By.TAG_NAME, "td")
            for cell in cells:
                if is_date(cell.text):
                    row_data.append(format_date(cell.text))
                else:
                    row_data.append(cell.text)
            transactions.append(row_data)
        return transactions

    def check_transactions_and_write_csv(self, fibonacci, timeout=10):
        transactions = self.get_transactions(timeout)
        last_two_rows = transactions[-2:]

        pre_last_row_values = last_two_rows[0]
        last_row_values = last_two_rows[1]

        if (last_row_values[0] > pre_last_row_values[0] and
                int(last_row_values[1]) == int(pre_last_row_values[1]) == fibonacci and
                pre_last_row_values[2] == "Credit" and
                last_row_values[2] == "Debit"):
            write_csv(transactions)

    def get_balance(self, timeout=10):
        center_div_locator = (By.XPATH, '(//div[@class="center"])[1]')
        center_div = self.wait_for_element(
            ec.presence_of_element_located(center_div_locator),
            timeout,
        )
        strong_elements_locator = (By.TAG_NAME, 'strong')
        strong_elements = center_div.find_elements(*strong_elements_locator)

        if len(strong_elements) >= 2:
            balance_value = strong_elements[1].text
            return int(balance_value)
        else:
            return None

