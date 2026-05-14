from playwright.sync_api import Page
import allure


class PracticePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.product_cards = page.locator(".products > .product")

    def navigate(self, url: str):
        self.page.goto(url)

    def click_radio_button_example(self, option_label: int):
        if '1' in str(option_label):
            radio_value = 'radio1'
        elif '2' in str(option_label):
            radio_value = 'radio2'
        elif '3' in str(option_label):
            radio_value = 'radio3'
        else:
            raise Exception("Invalid radio button label.")
        with allure.step("Click radio button example"):
            self.page.locator(f"input[value='{radio_value}']").click()

    def get_radio_button_example_status(self, option_label: str) -> bool:
        if '1' in str(option_label):
            radio_value = 'radio1'
        elif '2' in str(option_label):
            radio_value = 'radio2'
        elif '3' in str(option_label):
            radio_value = 'radio3'
        else:
            raise Exception("Invalid radio button label.")
        with allure.step("Get checked radio button status"):
            radio = self.page.locator(f"input[type='radio'][value='{radio_value}']")
            return radio.is_checked()

    def input_suggestion_class_example(self, text: str):
        '''Clicks the first option in the suggestion list after typing into it.'''
        with allure.step("Input text into suggestion class example"):
            self.page.fill("#autocomplete", text)
            self.page.wait_for_selector(".ui-menu-item")
            self.page.locator(".ui-menu-item").first.click()

    def get_suggestion_class_example(self) -> str:
        with allure.step("Get suggestion class example text"):
            return self.page.input_value("#autocomplete")

    def select_dropdown_example(self, text: str):
        with allure.step("Select dropdown option by Label|Value"):
            self.page.select_option("#dropdown-class-example", text)

    def get_dropdown_example_selected_option(self) -> str:
        with allure.step("Get selected dropdown option"):
            selected_option = self.page.locator("#dropdown-class-example option:checked")
            return selected_option.text_content().strip()
    
    def check_checkbox_example_by_value(self, checkbox_value: str, check: bool):
        if '1' in str(checkbox_value):
            checkbox_value = 'option1'
        elif '2' in str(checkbox_value):
            checkbox_value = 'option2'
        elif '3' in str(checkbox_value):
            checkbox_value = 'option3'
        else:
            raise Exception("Invalid checkbox value.")
        with allure.step("Check checkbox example"):
            if check:
                self.page.locator(f"input[type='checkbox'][value='{checkbox_value}']").check()
            else:
                self.page.locator(f"input[type='checkbox'][value='{checkbox_value}']").uncheck()

    def get_checkbox_example_checked_status(self, checkbox_value: str) -> bool:
        if '1' in str(checkbox_value):
            checkbox_value = 'option1'
        elif '2' in str(checkbox_value):
            checkbox_value = 'option2'
        elif '3' in str(checkbox_value):
            checkbox_value = 'option3'
        else:
            raise Exception("Invalid checkbox value.")
        with allure.step("Get checked checkbox status"):
            checkbox = self.page.locator(f"input[type='checkbox'][value='{checkbox_value}']")
            return checkbox.is_checked()
            