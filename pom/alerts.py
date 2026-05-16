from playwright.sync_api import Page, Dialog
from typing import Callable


class AlertHandler:
    _active_handlers: dict = {}

    @classmethod
    def enable_alert_auto_handling(cls, page: Page, action: str = 'accept') -> None:
        """Auto-handle all dialogs on this page until disable_alert_auto_handling() is called."""
        cls.disable_alert_auto_handling(page)

        def handler(d: Dialog) -> None:
            d.accept() if action == 'accept' else d.dismiss()

        cls._active_handlers[id(page)] = handler
        page.on('dialog', handler)

    @classmethod
    def disable_alert_auto_handling(cls, page: Page) -> None:
        """Stop auto-handling dialogs on this page."""
        handler = cls._active_handlers.pop(id(page), None)
        if handler:
            page.remove_listener('dialog', handler)

    @staticmethod
    def click_and_accept(page: Page, trigger: Callable) -> Dialog:
        """Click trigger(), accept the resulting dialog, and return it for message inspection."""
        captured = []

        def handle(d: Dialog) -> None:
            captured.append(d)
            d.accept()

        page.once('dialog', handle)
        trigger()
        return captured[0]

    @staticmethod
    def click_and_dismiss(page: Page, trigger: Callable) -> Dialog:
        """Click trigger(), dismiss the resulting dialog, and return it for message inspection."""
        captured = []

        def handle(d: Dialog) -> None:
            captured.append(d)
            d.dismiss()

        page.once('dialog', handle)
        trigger()
        return captured[0]
