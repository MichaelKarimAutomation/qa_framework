import pytest
import allure
from pom.practice_page import PracticePage


@allure.feature('UI Testing')
@allure.story('Interact with all elements on the practice page')
@pytest.mark.ui
@pytest.mark.regression
def test_practice_page_interactions(page, practice_url):
    practice = PracticePage(page)
    practice.navigate(practice_url)

    with allure.step('Verify radio button interaction'):
        practice.click_radio_button_example(2)
        practice.click_radio_button_example(3)
        practice.click_radio_button_example(1)
        radio1_status = practice.get_radio_button_example_status('1')
        radio2_status = practice.get_radio_button_example_status('2')
        radio3_status = practice.get_radio_button_example_status('3')

        practice.input_suggestion_class_example('New Zeal')
        suggestion_text = practice.get_suggestion_class_example()

        practice.select_dropdown_example('Option2')
        practice.select_dropdown_example('Option1')
        practice.select_dropdown_example('option3')
        selected_option = practice.get_dropdown_example_selected_option()

        practice.check_checkbox_example_by_value('1', True)
        practice.check_checkbox_example_by_value('2', False)
        practice.check_checkbox_example_by_value('3', True)
        practice.check_checkbox_example_by_value('3', False)
        practice.check_checkbox_example_by_value('3', True)
        checked_value1_status = practice.get_checkbox_example_checked_status('1')
        checked_value2_status = practice.get_checkbox_example_checked_status('2')
        checked_value3_status = practice.get_checkbox_example_checked_status('3')

        assert radio1_status is True
        assert radio2_status is False
        assert radio3_status is False

        assert suggestion_text == 'New Zealand'

        assert selected_option == 'Option3'

        assert checked_value1_status is True
        assert checked_value2_status is False
        assert checked_value3_status is True

        starting_url = practice.page.url
        assert 1 == len(page.context.pages)

        window_page = practice.click_open_window_and_return_page_instance()
        assert starting_url != window_page.url
        assert 2 == len(page.context.pages)

        tab_page = practice.click_open_tab_and_return_page_instance()
        assert starting_url != tab_page
        assert 3 == len(page.context.pages)

        window_page.close()
        tab_page.close()

        assert 1 == len(page.context.pages)

        alert_dialog = practice.click_alert_and_return_dialog()
        assert alert_dialog.message == 'Hello , share this practice page and share your knowledge'

        practice.click_confirm()

        practice.click_hide_example()
        hidden_status = practice.get_element_displayed_example_visibility()
        practice.click_show_example()
        shown_status = practice.get_element_displayed_example_visibility()

        practice.hover_mouse_hover_example()
        practice.click_top_hover_option()

        iframe_course = practice.get_iframe_course_name()

        assert hidden_status is False
        assert shown_status is True

        assert 'courses' in iframe_course.lower()
