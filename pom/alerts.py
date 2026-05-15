from playwright.sync_api import Page, TimeoutError
import allure


class AlertHandler:
    @staticmethod
    def expect_alert(page: Page, timeout: int = 5000):
        """
        Wait for an alert dialog to appear within the specified timeout.
        Raises TimeoutError if no alert appears.
        Returns the dialog object if it appears.
        """
        with allure.step(f"Expect alert to appear within {timeout}ms"):
            with page.expect_event("dialog", timeout=timeout) as event_info:
                pass
            return event_info.value

    @staticmethod
    def accept_alert(dialog):
        """
        Accept the given alert dialog.
        """
        with allure.step("Accept alert"):
            dialog.accept()

    @staticmethod
    def dismiss_alert(dialog):
        """
        Dismiss the given alert dialog.
        """
        with allure.step("Dismiss alert"):
            dialog.dismiss()

    @staticmethod
    def setup_alert_listener(page: Page, action: str = 'accept'):
        """
        Set up a listener for alert dialogs.
        action: 'accept' or 'dismiss'
        Returns the handler function so it can be removed later with page.off('dialog', handler)
        """
        def handler(dialog):
            if action.lower() == 'accept':
                AlertHandler.accept_alert(dialog)
            elif action.lower() == 'dismiss':
                AlertHandler.dismiss_alert(dialog)
            else:
                raise ValueError("Action must be 'accept' or 'dismiss'")

        page.on('dialog', handler)
        return handler
    