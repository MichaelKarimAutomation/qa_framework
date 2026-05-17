import allure
from playwright.sync_api import Page, Dialog
from pom.alerts import AlertHandler


class PracticePage:
    def __init__(self, page: Page) -> None:
        """Initialize the practice page wrapper and define locators for its static UI elements."""
        self.page = page
        self.suggestion_items = page.locator('.ui-menu-item')
        self.dropdown_selected_option = page.locator('#dropdown-class-example option:checked')
        self.open_window_button = page.locator('#openwindow')
        self.open_tab_button = page.locator('#opentab')
        self.alert_button = page.locator("input[value='Alert']")
        self.confirm_button = page.locator("input[value='Confirm']")
        self.hide_button = page.locator('#hide-textbox')
        self.show_button = page.locator('#show-textbox')
        self.displayed_textbox = page.locator('#displayed-text')
        self.mouse_hover_trigger = page.locator('#mousehover')
        self.top_hover_option = page.locator(".mouse-hover-content a[href='#top']")
        self.reload_hover_option = page.locator(".mouse-hover-content a[href='']")
        self.courses_iframe = page.frame_locator('#courses-iframe')

    def navigate(self, url: str):
        """Open the practice page at the given URL in the browser."""
        self.page.goto(url)

    def click_radio_button_example(self, option_label: int):
        """Click radio button 1, 2, or 3 in the radio example (label may be int or string containing the digit)."""
        if '1' in str(option_label):
            radio_value = 'radio1'
        elif '2' in str(option_label):
            radio_value = 'radio2'
        elif '3' in str(option_label):
            radio_value = 'radio3'
        else:
            raise Exception('Invalid radio button label.')
        with allure.step('Click radio button example'):
            self.page.locator(f"input[value='{radio_value}']").click()

    def get_radio_button_example_status(self, option_label: str) -> bool:
        """Return True if the radio button identified by label 1, 2, or 3 is currently selected."""
        if '1' in str(option_label):
            radio_value = 'radio1'
        elif '2' in str(option_label):
            radio_value = 'radio2'
        elif '3' in str(option_label):
            radio_value = 'radio3'
        else:
            raise Exception('Invalid radio button label.')
        with allure.step('Get checked radio button status'):
            radio = self.page.locator(f"input[type='radio'][value='{radio_value}']")
            return radio.is_checked()

    def input_suggestion_class_example(self, text: str):
        """Type into the autocomplete input and click the first matching suggestion that appears."""
        with allure.step('Input text into suggestion class example'):
            self.page.fill('#autocomplete', text)
            self.page.wait_for_selector('.ui-menu-item')
            self.suggestion_items.first.click()

    def get_suggestion_class_example(self) -> str:
        """Return the current text value of the autocomplete input field."""
        with allure.step('Get suggestion class example text'):
            return self.page.input_value('#autocomplete')

    def select_dropdown_example(self, text: str):
        """Select an option in the dropdown example by its label or value."""
        with allure.step('Select dropdown option by Label|Value'):
            self.page.select_option('#dropdown-class-example', text)

    def get_dropdown_example_selected_option(self) -> str:
        """Return the visible text of the option currently selected in the dropdown example."""
        with allure.step('Get selected dropdown option'):
            return self.dropdown_selected_option.inner_text().strip()

    def check_checkbox_example_by_value(self, checkbox_value: str, check: bool):
        """Check or uncheck checkbox 1, 2, or 3 in the checkbox example based on the `check` flag."""
        if '1' in str(checkbox_value):
            checkbox_value = 'option1'
        elif '2' in str(checkbox_value):
            checkbox_value = 'option2'
        elif '3' in str(checkbox_value):
            checkbox_value = 'option3'
        else:
            raise Exception('Invalid checkbox value.')
        with allure.step('Check checkbox example'):
            if check:
                self.page.locator(f"input[type='checkbox'][value='{checkbox_value}']").check()
            else:
                self.page.locator(f"input[type='checkbox'][value='{checkbox_value}']").uncheck()

    def get_checkbox_example_checked_status(self, checkbox_value: str) -> bool:
        """Return True if the checkbox identified by value 1, 2, or 3 is currently checked."""
        if '1' in str(checkbox_value):
            checkbox_value = 'option1'
        elif '2' in str(checkbox_value):
            checkbox_value = 'option2'
        elif '3' in str(checkbox_value):
            checkbox_value = 'option3'
        else:
            raise Exception('Invalid checkbox value.')
        with allure.step('Get checked checkbox status'):
            checkbox = self.page.locator(f"input[type='checkbox'][value='{checkbox_value}']")
            return checkbox.is_checked()

    def click_open_window_and_return_page_instance(self):
        """Click the 'Open Window' button and return the Playwright Page object for the popup window."""
        with allure.step('Click open window and return new window page'):
            with self.page.expect_popup() as popup_info:
                self.open_window_button.click()
            return popup_info.value

    def click_open_tab_and_return_page_instance(self):
        """Click the 'Open Tab' button and return the Playwright Page object for the new browser tab."""
        with allure.step('Click open tab and return new tab page'):
            with self.page.context.expect_page() as new_page_info:
                self.open_tab_button.click()
            return new_page_info.value

    def click_alert_and_return_dialog(self) -> Dialog:
        """Click the 'Alert' button, accept the resulting JS dialog, and return it for message inspection."""
        with allure.step('Click switch to alert example'):
            return AlertHandler.click_and_accept(self.page, lambda: self.alert_button.click())

    def click_confirm(self):
        """Click the 'Confirm' button (the caller is responsible for handling the resulting dialog)."""
        with allure.step('Click confirm example'):
            self.confirm_button.click()

    def click_hide_example(self):
        """Click the 'Hide' button to hide the displayed textbox in the show/hide example."""
        with allure.step('Click hide example'):
            self.hide_button.click()

    def click_show_example(self):
        """Click the 'Show' button to reveal the hidden textbox in the show/hide example."""
        with allure.step('Click show example'):
            self.show_button.click()

    def get_element_displayed_example_visibility(self) -> bool:
        """Return True if the textbox in the show/hide example is currently visible on the page."""
        with allure.step('Get element displayed example visibility'):
            return self.displayed_textbox.is_visible()

    def hover_mouse_hover_example(self):
        """Hover the mouse over the mouse-hover trigger to reveal its dropdown menu."""
        with allure.step('Hover mouse hover example'):
            self.mouse_hover_trigger.hover()

    def click_top_hover_option(self):
        """Click the 'Top' link inside the mouse-hover dropdown (anchors back to top of page)."""
        with allure.step('Click top hover option'):
            self.top_hover_option.click()

    def click_reload_hover_option(self):
        """Click the 'Reload' link inside the mouse-hover dropdown (reloads the page)."""
        with allure.step('Click reload hover option'):
            self.reload_hover_option.click()

    def switch_to_iframe_example(self):
        """Return a FrameLocator pointing at the courses iframe so its contents can be queried."""
        with allure.step('Switch to iframe example'):
            return self.courses_iframe

    def get_iframe_course_name(self) -> str:
        """Return the text of the courses heading inside the iframe, falling back to the first h2 if not found by text."""
        with allure.step('Get iframe course name'):
            iframe = self.switch_to_iframe_example()
            heading = iframe.locator('h2', has_text='Courses').first
            if heading.count() == 0:
                heading = iframe.locator('h2').first
            return heading.inner_text().strip()
