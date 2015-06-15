# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import By, expected, Wait
from marionette.keys import Keys

from marketplacetests.marketplace.app import Marketplace


class BasePage(Marketplace):

    _body_loaded_locator = (By.CSS_SELECTOR, 'body.loaded')
    # This allows us to instantiate a base page object no matter which page we are currently on
    _page_loaded_locator = (By.CSS_SELECTOR, 'body.loaded')
    _nav_menu_toggle_locator = (By.CSS_SELECTOR, 'mkt-nav-toggle button')
    _home_button_locator = (By.CSS_SELECTOR, 'h1.site a')
    _notification_locator = (By.ID, 'notification-content')

    # Marketplace search on home page
    _search_toggle_locator = (By.CSS_SELECTOR, '.header--search-toggle')
    _search_input_locator = (By.ID, 'search-q')

    _signed_in_notification_locator = (By.CSS_SELECTOR, '#notification.show')

    # System app install notification message
    _install_notification_locator = (By.CSS_SELECTOR, '.banner.generic-dialog > p')

    def __init__(self, marionette):
        Marketplace.__init__(self, marionette)
        self.wait_for_page_loaded()

    def login(self, username, password):
        ff_accounts = self.show_menu().tap_sign_in()
        ff_accounts.login(username, password)
        self.switch_to_marketplace_frame()
        self.wait_for_login_success_notification()

    @property
    def first_free_app(self):
        free_apps = self.search(':free').search_results
        app = free_apps[0]
        app_dict = {'name': app.name, 'author': app.author}
        self.tap_home()
        return app_dict

    def wait_for_notification_message(self, message):
        """This will wait for the specified message to appear in the DOM element
           for the notification message, not for that message to be visible.

           This is required as often the message is no longer visible when we check,
           but the expected text still exists in the DOM element.

           This is also the reason that we wait for the element to no longer be
           visible at the end of this method, whereas we do not wait for it to
           first be visible.
        """
        element = self.marionette.find_element(*self._notification_locator)
        Wait(self.marionette).until(self._element_inner_html_contains(element, message))
        Wait(self.marionette).until(expected.element_not_displayed(element))

    class _element_inner_html_contains(object):

        def __init__(self, element, text):
            self.element = element
            self.needle = text

        def __call__(self, marionette):
            haystack = marionette.execute_script('return arguments[0].innerHTML;', [self.element])
            marionette.log('Looking for "%s" in "%s"' % (self.needle, haystack))
            return self.needle in haystack

    def wait_for_login_success_notification(self):
        self.wait_for_notification_message('You have been signed in')

    def wait_for_region_updated_notification(self, region):
        self.wait_for_notification_message('Region updated to %s' % region)

    def wait_for_page_loaded(self):
        Wait(self.marionette).until(
            expected.element_present(*self._body_loaded_locator))
        Wait(self.marionette).until(
            expected.element_present(*self._page_loaded_locator))

    def _perform_search(self, term):
        self.marionette.find_element(*self._search_toggle_locator).tap()
        search_box = Wait(self.marionette).until(
            expected.element_present(*self._search_input_locator))
        Wait(self.marionette).until(expected.element_displayed(search_box))
        search_box.send_keys(term)
        search_box.send_keys(Keys.RETURN)

    def search(self, term):
        self._perform_search(term)
        from marketplacetests.marketplace.pages.search_results import SearchResults
        return SearchResults(self.marionette)

    def set_region(self, region):
        self._perform_search(':debug')
        from marketplacetests.marketplace.pages.debug import Debug
        debug_screen = Debug(self.marionette)
        debug_screen.select_region(region)
        # wait for notification of the change
        self.wait_for_region_updated_notification(region)

        debug_screen.tap_back()
        self.wait_for_page_loaded()

    def navigate_to_app(self, app_name):
        search_results = self.search(app_name).search_results
        for result in search_results:
            if result.name == app_name:
                return result.tap_app()

        # app not found
        raise Exception('The app: %s was not found.' % app_name)

    def tap_home(self):
        self.marionette.find_element(*self._home_button_locator).tap()

    @property
    def install_notification_message(self):
        self.marionette.switch_to_frame()
        self.wait_for_element_displayed(*self._install_notification_locator)
        return self.marionette.find_element(*self._install_notification_locator).text

    def show_menu(self):
        self.marionette.find_element(*self._nav_menu_toggle_locator).tap()
        body = self.marionette.find_element(By.TAG_NAME, 'body')
        Wait(self.marionette).until(
            lambda m: 'mkt-nav--visible' in body.get_attribute('class'))
        return NavMenu(self.marionette)

    def search_for_paid_apps(self):
        self.set_region('United States')
        return self.search(':paid')

    def is_app_installed(self, name):
        installed = self.apps.is_app_installed(name)
        self.switch_to_marketplace_frame()
        return installed

    def wait_for_payment_cancelled_notification(self):
        self.wait_for_notification_message('Payment cancelled.')


class NavMenu(Marketplace):

    _feedback_menu_item_locator = (By.CSS_SELECTOR, '.mkt-nav--link[href*="feedback"]')
    _settings_menu_item_locator = (By.CSS_SELECTOR, '.mkt-nav--link[href*="settings"]')
    _sign_in_menu_item_locator = (By.CSS_SELECTOR, '.mkt-nav--link.persona:not(.register)')

    def tap_settings(self):
        settings_item = self.marionette.find_element(*self._settings_menu_item_locator)
        Wait(self.marionette).until(expected.element_displayed(settings_item))
        settings_item.tap()
        from marketplacetests.marketplace.pages.settings import Settings
        return Settings(self.marionette)

    def tap_feedback(self):
        feedback_item = self.marionette.find_element(*self._feedback_menu_item_locator)
        Wait(self.marionette).until(expected.element_displayed(feedback_item))
        feedback_item.tap()
        from marketplacetests.marketplace.pages.feedback import Feedback
        return Feedback(self.marionette)

    def tap_sign_in(self):
        sign_in_item = self.marionette.find_element(*self._sign_in_menu_item_locator)
        Wait(self.marionette).until(expected.element_displayed(sign_in_item))
        sign_in_item.tap()
        from marketplacetests.firefox_accounts.app import FirefoxAccounts
        return FirefoxAccounts(self.marionette)
